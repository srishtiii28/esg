from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict
import uvicorn
import hashlib
import asyncio
import datetime
import os
from ai.document_processor import DocumentProcessor
from ai.esg_analyzer import ESGAnalyzer
from ai.greenwashing_detector import GreenwashingDetector
from ai.report_summarizer import ReportSummarizer
from models.schemas import ESGScore

app = FastAPI(
    title="GreenStamp API",
    description="AI + Blockchain-powered ESG Analysis Platform",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI components
esg_analyzer = ESGAnalyzer()
greenwashing_detector = GreenwashingDetector()
report_summarizer = ReportSummarizer()
doc_processor = DocumentProcessor()

@app.get("/")
async def root():
    return {"message": "Welcome to GreenStamp API"}

@app.post("/analyze")
async def analyze_report(file: UploadFile = File(...)):
    try:
        print(f"Received file: {file.filename}")
        print(f"File content type: {file.content_type}")
        
        # Check file size
        content = await file.read()
        file_size = len(content)
        print(f"File size: {file_size} bytes")
        
        if file_size > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(status_code=400, detail="File too large")

        # Create temporary file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_dir = "/tmp/greenstamp"
        os.makedirs(temp_dir, exist_ok=True)
        temp_file = os.path.join(temp_dir, f"{timestamp}_{file.filename}")
        print(f"Saving file to: {temp_file}")
        
        try:
            # Save file
            with open(temp_file, "wb") as f:
                f.write(content)
            print("File saved successfully")

            # Extract text
            print("Starting text extraction...")
            text_results = doc_processor.extract_text(temp_file)
            text = " ".join(text_results.values())
            print(f"Extracted text length: {len(text)} characters")
            
            if not text or not text.strip():
                raise HTTPException(status_code=400, detail="No text extracted")
            
            # Analyze ESG content
            print("Starting ESG analysis...")
            esg_results = esg_analyzer.analyze_text(text)
            print("ESG analysis completed")
            
            # Generate summary
            print("Generating summary...")
            summary_results = report_summarizer.summarize(text)
            print("Summary generated")
            
            # Calculate document hash
            doc_hash = hashlib.sha256(content).hexdigest()
            print(f"Document hash: {doc_hash}")
            
            # Create response
            response = {
                "environmental": float(esg_results["scores"]["environmental"]),
                "social": float(esg_results["scores"]["social"]),
                "governance": float(esg_results["scores"]["governance"]),
                "total": float(esg_results["scores"]["total"]),
                "report_hash": doc_hash,
                "analysis": {
                    "scores": esg_results["scores"],
                    "category_details": esg_results["category_details"],
                    "summary": summary_results,
                    "text_excerpt": text[:1000] + "..." if len(text) > 1000 else text,
                    "metadata": {
                        "filename": file.filename,
                        "file_size": str(file_size),
                        "analyzed_at": datetime.datetime.now().isoformat(),
                        "document_type": file.filename.split('.')[-1].lower(),
                        "model_version": "esg-analyzer-v1"
                    }
                }
            }
            print("Response created successfully")
            return response
            
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)
                print("Temporary file cleaned up")
                
    except HTTPException as e:
        print(f"HTTP Exception: {str(e)}")
        raise e
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8002, reload=True)
