from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn
import hashlib
import asyncio
import datetime
from ai import OCRProcessor, ESGAnalyzer

app = FastAPI(title="GreenStamp API", description="AI + Blockchain-powered ESG Analysis Platform")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI components
ocr_processor = OCRProcessor()
esg_analyzer = ESGAnalyzer()

class CategoryScore(BaseModel):
    """Detailed score for an ESG subcategory"""
    score: float
    evidence: Optional[str] = None

class CategoryAnalysis(BaseModel):
    """Analysis of specific ESG categories"""
    subcategories: Dict[str, float]

class ReportSummary(BaseModel):
    """Summary of the ESG report"""
    brief: str
    full: str
    length: int
    compression_ratio: float

class GreenwashingWarning(BaseModel):
    """Warning for potential greenwashing"""
    type: str
    description: str
    confidence: float
    severity: str
    text_snippet: Optional[str] = None

class ESGCategoryDetails(BaseModel):
    """ESG category details"""
    environmental: Dict[str, float]
    social: Dict[str, float]
    governance: Dict[str, float]

class ESGAnalysisResult(BaseModel):
    """Detailed ESG analysis results"""
    scores: Dict[str, float] = {
        'environmental': 0.0,
        'social': 0.0,
        'governance': 0.0,
        'total': 0.0
    }
    category_details: Dict[str, Dict[str, float]] = {
        'environmental': {},
        'social': {},
        'governance': {}
    }
    greenwashing_warnings: List[GreenwashingWarning] = []
    summary: Dict[str, any] = {
        'brief': '',
        'full': '',
        'length': 0,
        'compression_ratio': 1.0
    }
    text_excerpt: str = ''
    metadata: Dict[str, str] = {}

class ESGScore(BaseModel):
    """Complete ESG analysis response"""
    environmental: float
    social: float
    governance: float
    total: float
    report_hash: str
    ipfs_url: Optional[str] = None
    analysis: ESGAnalysisResult

@app.get("/")
async def root():
    return {"message": "Welcome to GreenStamp API"}

@app.post("/analyze", response_model=ESGScore)
async def analyze_report(file: UploadFile = File(...)):
    """
    Analyze an ESG report and return comprehensive analysis with blockchain verification
    
    Parameters:
    - file: PDF or text document containing the ESG report
    
    Returns:
    - ESGScore object containing:
        - Overall ESG scores (environmental, social, governance, total)
        - Detailed category analysis
        - Greenwashing detection warnings
        - Report summary
        - Blockchain verification details
    
    Example usage with Python requests:
    ```python
    import requests
    
    url = "http://localhost:8000/analyze"
    files = {"file": open("esg_report.pdf", "rb")}
    response = requests.post(url, files=files)
    result = response.json()
    
    # Access results
    total_score = result["total"]
    env_details = result["analysis"]["category_details"]["environmental"]
    warnings = result["analysis"]["greenwashing_warnings"]
    summary = result["analysis"]["summary"]["brief"]
    ```
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")

    # Check file size (max 10MB)
    file_size = 0
    content = await file.read()
    file_size = len(content)
    if file_size > 10 * 1024 * 1024:  # 10MB
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 10MB")

    try:
        if not content:
            raise HTTPException(status_code=400, detail="Empty file provided")

        # Extract text using OCR
        text = await ocr_processor.extract_text(content, file.filename)
        if not text or not text.strip():
            raise HTTPException(status_code=400, detail="No text could be extracted from the file")
        
        # Calculate document hash
        hasher = hashlib.sha256()
        hasher.update(content)
        doc_hash = hasher.hexdigest()
        
        # Analyze ESG content
        scores = await esg_analyzer.analyze_text(text)
        if not scores:
            raise HTTPException(status_code=500, detail="Failed to analyze ESG content")
        
        # Detect greenwashing
        try:
            warnings = await esg_analyzer.detect_greenwashing(text)
        except Exception as e:
            print(f"Warning: Error detecting greenwashing: {str(e)}")
            warnings = []
        
        # Generate summary
        try:
            summary = await esg_analyzer.generate_summary(text)
        except Exception as e:
            print(f"Warning: Error generating summary: {str(e)}")
            summary = {
                'brief': 'Error generating summary',
                'full': 'Error generating summary',
                'length': len(text),
                'compression_ratio': 1.0
            }
        
        # Prepare category analysis
        try:
            category_analysis = await esg_analyzer._analyze_categories(text)
        except Exception as e:
            print(f"Warning: Error analyzing categories: {str(e)}")
            category_analysis = {}
        
        # Create response
        # Create final response
        response = ESGScore(
            environmental=float(scores.get('environmental', 0.0)),
            social=float(scores.get('social', 0.0)),
            governance=float(scores.get('governance', 0.0)),
            total=float(scores.get('total', 0.0)),
            report_hash=doc_hash,
            analysis=ESGAnalysisResult(
                scores={k: float(v) for k, v in scores.items()},
                category_details=category_analysis,
                greenwashing_warnings=warnings,
                summary=summary,
                text_excerpt=text[:1000] + '...' if len(text) > 1000 else text,
                metadata={
                    'filename': file.filename,
                    'file_size': str(len(content)),
                    'analyzed_at': datetime.datetime.now().isoformat(),
                    'document_type': file.filename.split('.')[-1].lower(),
                    'model_version': 'finbert-esg-v2'
                }
            )
        )
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
