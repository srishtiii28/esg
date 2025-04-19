"""Pydantic models for API schemas"""

from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class CategoryScore(BaseModel):
    """Score for an ESG subcategory"""
    score: float
    evidence: Optional[str] = None

class CategoryAnalysis(BaseModel):
    """Analysis of specific ESG categories"""
    subcategories: Dict[str, float]

class GreenwashingWarning(BaseModel):
    """Warning for potential greenwashing"""
    type: str
    description: str
    confidence: float
    severity: str
    text_snippet: Optional[str] = None

class ReportSummary(BaseModel):
    """Summary of the ESG report"""
    brief: str
    full: str
    length: int
    compression_ratio: float

class ESGAnalysisResult(BaseModel):
    """Detailed ESG analysis results"""
    scores: Dict[str, float]
    category_details: Dict[str, Dict[str, float]]
    greenwashing_warnings: List[GreenwashingWarning]
    summary: Dict[str, str]
    text_excerpt: str
    metadata: Dict[str, str]

class ESGScore(BaseModel):
    """Complete ESG analysis response"""
    environmental: float
    social: float
    governance: float
    total: float
    report_hash: str
    analysis: ESGAnalysisResult
