from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn
import hashlib
import asyncio
import datetime
import os
from ai.document_processor import DocumentProcessor
from ai.esg_analyzer import ESGAnalyzer
from ai.greenwashing_detector import GreenwashingDetector
from ai.report_summarizer import ReportSummarizer

app = FastAPI(
    title="GreenStamp API",
    description="AI + Blockchain-powered ESG Analysis Platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create API router
router = APIRouter(
    tags=["analysis"],
    responses={404: {"description": "Not found"}}
)

# Initialize AI components
doc_processor = DocumentProcessor()
esg_analyzer = ESGAnalyzer()
greenwashing_detector = GreenwashingDetector()
report_summarizer = ReportSummarizer()

@router.get("/", tags=["health"])
async def health_check():
    return {"status": "ok"}

@app.get("/api")
async def root_api():
    return {"status": "ok"}

from typing import Any, Dict, List, Optional

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
    summary: Dict[str, Any] = {
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

@router.post("/analyze", response_model=ESGScore)
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
    
    url = "http://localhost:8002/api/analyze"
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
    try:
        # Log the incoming request
        print(f"Received file upload request for: {file.filename}")
        print(f"File size: {len(await file.read())} bytes")
        await file.seek(0)  # Reset file pointer after reading size

        # Check file size (max 10MB)
        content = await file.read()
        file_size = len(content)
        if file_size > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(status_code=400, detail="File too large. Maximum size is 10MB")

        if not content:
            raise HTTPException(status_code=400, detail="Empty file provided")

        # Extract text using our document processor
        try:
            # Save the uploaded file temporarily
            temp_file_path = f"temp_{file.filename}"
            print(f"Saving file to: {temp_file_path}")
            with open(temp_file_path, "wb") as f:
                f.write(content)
            
            # Process the file
            print(f"Processing file: {temp_file_path}")
            text_results = doc_processor.extract_text(temp_file_path)
            
            # Combine text from all pages
            text = " ".join(text_results.values())
            print(f"Extracted text length: {len(text)}")
            
            # Clean up
            os.remove(temp_file_path)
            print(f"Cleaned up temporary file: {temp_file_path}")
            
            if not text or not text.strip():
                raise HTTPException(status_code=400, detail="No text could be extracted from the file")

            # Calculate document hash
            hasher = hashlib.sha256()
            hasher.update(content)
            doc_hash = hasher.hexdigest()

            # Analyze ESG content
            try:
                esg_results = esg_analyzer.analyze_text(text)
                if not esg_results:
                    raise HTTPException(status_code=500, detail="Failed to analyze ESG content")
            except Exception as e:
                print(f"Error analyzing ESG content: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Error analyzing ESG content: {str(e)}")

            # Detect greenwashing
            try:
                greenwashing_results = greenwashing_detector.analyze_text(text)
            except Exception as e:
                print(f"Warning: Error detecting greenwashing: {str(e)}")
                greenwashing_results = {
                    "risk_score": 0.0,
                    "indicators": [],
                    "recommendations": []
                }

            # Generate summary
            try:
                summary_results = report_summarizer.summarize(text)
            except Exception as e:
                print(f"Warning: Error generating summary: {str(e)}")
                summary_results = {
                    "executive_summary": "Error generating summary",
                    "key_points": [],
                    "section_summaries": {},
                    "recommendations": []
                }

            # Create response
            response = ESGScore(
                environmental=float(esg_results["scores"]["environmental"]),
                social=float(esg_results["scores"]["social"]),
                governance=float(esg_results["scores"]["governance"]),
                total=float(esg_results["scores"]["overall"]),
                report_hash=doc_hash,
                analysis=ESGAnalysisResult(
                    scores=esg_results["scores"],
                    category_details={
                        "environmental": esg_results["key_topics"],
                        "social": [],
                        "governance": []
                    },
                    greenwashing_warnings=[
                        {
                            "type": indicator["type"],
                            "description": indicator["type"].replace("_", " ").title(),
                            "confidence": float(indicator["confidence"]),
                            "severity": indicator["severity"],
                            "text_snippet": None
                        }
                        for indicator in greenwashing_results["indicators"]
                    ],
                    summary={
                        "brief": summary_results["executive_summary"],
                        "full": summary_results["executive_summary"],
                        "length": len(text),
                        "compression_ratio": 1.0
                    },
                    text_excerpt=text[:1000] + '...' if len(text) > 1000 else text,
                    metadata={
                        'filename': file.filename,
                        'file_size': str(len(content)),
                        'analyzed_at': datetime.datetime.now().isoformat(),
                        'document_type': file.filename.split('.')[-1].lower(),
                        'model_version': 'esg-analyzer-v1'
                    }
                )
            )
            print(f"Successfully processed file: {file.filename}")
            return response

        except ValueError as e:
            print(f"Detailed error in main handler: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            print(f"Detailed error in main handler: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

        if not content:
            raise HTTPException(status_code=400, detail="Empty file provided")

        # Extract text using our document processor
        try:
            # Save the uploaded file temporarily
            temp_file_path = f"temp_{file.filename}"
            print(f"Saving file to: {temp_file_path}")
            with open(temp_file_path, "wb") as f:
                f.write(content)
            
            # Process the file
            print(f"Processing file: {temp_file_path}")
            text_results = doc_processor.extract_text(temp_file_path)
            
            # Combine text from all pages
            text = " ".join(text_results.values())
            print(f"Extracted text length: {len(text)}")
            
            # Clean up
            os.remove(temp_file_path)
            print(f"Cleaned up temporary file: {temp_file_path}")
            
            if not text or not text.strip():
                raise HTTPException(status_code=400, detail="No text could be extracted from the file")

            # Calculate document hash
            hasher = hashlib.sha256()
            hasher.update(content)
            doc_hash = hasher.hexdigest()

            # Analyze ESG content
            try:
                esg_results = esg_analyzer.analyze_text(text)
                if not esg_results:
                    raise HTTPException(status_code=500, detail="Failed to analyze ESG content")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error analyzing ESG content: {str(e)}")

            # Detect greenwashing
            try:
                greenwashing_results = greenwashing_detector.analyze_text(text)
            except Exception as e:
                print(f"Warning: Error detecting greenwashing: {str(e)}")
                greenwashing_results = {
                    "risk_score": 0.0,
                    "indicators": [],
                    "recommendations": []
                }

            # Generate summary
            try:
                summary_results = report_summarizer.summarize(text)
            except Exception as e:
                print(f"Warning: Error generating summary: {str(e)}")
                summary_results = {
                    "executive_summary": "Error generating summary",
                    "key_points": [],
                    "section_summaries": {},
                    "recommendations": []
                }

            # Create response
            response = ESGScore(
                environmental=float(esg_results["scores"]["environmental"]),
                social=float(esg_results["scores"]["social"]),
                governance=float(esg_results["scores"]["governance"]),
                total=float(esg_results["scores"]["overall"]),
                report_hash=doc_hash,
                analysis=ESGAnalysisResult(
                    scores=esg_results["scores"],
                    category_details={
                        "environmental": esg_results["key_topics"],
                        "social": [],
                        "governance": []
                    },
                    greenwashing_warnings=[
                        {
                            "type": indicator["type"],
                            "description": indicator["type"].replace("_", " ").title(),
                            "confidence": float(indicator["confidence"]),
                            "severity": indicator["severity"],
                            "text_snippet": None
                        }
                        for indicator in greenwashing_results["indicators"]
                    ],
                    summary={
                        "brief": summary_results["executive_summary"],
                        "full": summary_results["executive_summary"],
                        "length": len(text),
                        "compression_ratio": 1.0
                    },
                    text_excerpt=text[:1000] + '...' if len(text) > 1000 else text,
                    metadata={
                        'filename': file.filename,
                        'file_size': str(len(content)),
                        'analyzed_at': datetime.datetime.now().isoformat(),
                        'document_type': file.filename.split('.')[-1].lower(),
                        'model_version': 'esg-analyzer-v1'
                    }
                )
            )
            return response

        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            print(f"Detailed error in text extraction: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error extracting text from file: {str(e)}")

        # Analyze ESG content
        try:
            esg_results = esg_analyzer.analyze_text(text)
            if not esg_results:
                raise HTTPException(status_code=500, detail="Failed to analyze ESG content")
        except Exception as e:
            print(f"Error analyzing ESG content: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error analyzing ESG content: {str(e)}")

        # Detect greenwashing
        try:
            greenwashing_results = greenwashing_detector.analyze_text(text)
        except Exception as e:
            print(f"Warning: Error detecting greenwashing: {str(e)}")
            greenwashing_results = {
                "risk_score": 0.0,
                "indicators": [],
                "recommendations": []
            }

        # Generate summary
        try:
            summary_results = report_summarizer.summarize(text)
        except Exception as e:
            print(f"Warning: Error generating summary: {str(e)}")
            summary_results = {
                "executive_summary": "Error generating summary",
                "key_points": [],
                "section_summaries": {},
                "recommendations": []
            }

        # Create response
        response = ESGScore(
            environmental=float(esg_results["scores"]["environmental"]),
            social=float(esg_results["scores"]["social"]),
            governance=float(esg_results["scores"]["governance"]),
            total=float(esg_results["scores"]["overall"]),
            report_hash=doc_hash,
            analysis=ESGAnalysisResult(
                scores=esg_results["scores"],
                category_details={
                    "environmental": esg_results["key_topics"],
                    "social": [],
                    "governance": []
                },
                greenwashing_warnings=[
                    {
                        "type": indicator["type"],
                        "description": indicator["type"].replace("_", " ").title(),
                        "confidence": float(indicator["confidence"]),
                        "severity": indicator["severity"],
                        "text_snippet": None
                    }
                    for indicator in greenwashing_results["indicators"]
                ],
                summary={
                    "brief": summary_results["executive_summary"],
                    "full": summary_results["executive_summary"],
                    "length": len(text),
                    "compression_ratio": 1.0
                },
                text_excerpt=text[:1000] + '...' if len(text) > 1000 else text,
                metadata={
                    'filename': file.filename,
                    'file_size': str(len(content)),
                    'analyzed_at': datetime.datetime.now().isoformat(),
                    'document_type': file.filename.split('.')[-1].lower(),
                    'model_version': 'esg-analyzer-v1'
                }
            )
        )

        print(f"Successfully processed file: {file.filename}")
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

# Mount the router
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="localhost", port=8002, reload=True)
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        log_level="info",
        workers=1
    )
