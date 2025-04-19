"""Report summarization module for generating concise ESG report summaries"""

from typing import Dict, List
from transformers import pipeline
import numpy as np
from nltk.tokenize import sent_tokenize
import nltk

class ReportSummarizer:
    def __init__(self):
        """Initialize the report summarizer with necessary models"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
            
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.key_points_extractor = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    def summarize(self, text: str) -> Dict:
        """Generate a comprehensive summary of the ESG report"""
        results = {
            "executive_summary": self._generate_executive_summary(text),
            "key_points": self._extract_key_points(text),
            "section_summaries": self._generate_section_summaries(text),
            "recommendations": self._generate_recommendations(text)
        }
        return results

    def _generate_executive_summary(self, text: str, max_length: int = 300) -> str:
        """Generate a concise executive summary"""
        # Split text into chunks that fit within model's max token limit
        chunks = self._split_text(text, max_length=1024)
        summaries = []
        
        for chunk in chunks:
            summary = self.summarizer(chunk, 
                                    max_length=150, 
                                    min_length=50,
                                    do_sample=False)
            summaries.append(summary[0]['summary_text'])
        
        # Combine and summarize again if needed
        final_summary = " ".join(summaries)
        if len(final_summary) > max_length:
            final_summary = self.summarizer(final_summary,
                                          max_length=max_length,
                                          min_length=max_length//2,
                                          do_sample=False)[0]['summary_text']
        
        return final_summary

    def _extract_key_points(self, text: str) -> List[Dict]:
        """Extract key points from the text"""
        # Categories to classify statements into
        categories = [
            "environmental_initiative",
            "social_responsibility",
            "governance_practice",
            "risk_management",
            "future_commitment",
            "achievement",
            "challenge"
        ]
        
        sentences = sent_tokenize(text)
        key_points = []
        
        for sentence in sentences:
            result = self.key_points_extractor(sentence, categories, multi_label=True)
            max_score = max(result['scores'])
            
            if max_score > 0.7:  # Only include high-confidence points
                key_points.append({
                    "point": sentence,
                    "category": result['labels'][result['scores'].index(max_score)],
                    "confidence": float(max_score)
                })
        
        # Sort by confidence and return top points
        key_points.sort(key=lambda x: x['confidence'], reverse=True)
        return key_points[:10]

    def _generate_section_summaries(self, text: str) -> Dict[str, str]:
        """Generate summaries for different sections of the report"""
        sections = {
            "environmental": self._extract_section(text, "environmental"),
            "social": self._extract_section(text, "social"),
            "governance": self._extract_section(text, "governance")
        }
        
        summaries = {}
        for section, content in sections.items():
            if content:
                summary = self.summarizer(content,
                                        max_length=200,
                                        min_length=50,
                                        do_sample=False)[0]['summary_text']
                summaries[section] = summary
        
        return summaries

    def _generate_recommendations(self, text: str) -> List[str]:
        """Generate recommendations based on the report content"""
        # Simple recommendation generation based on key points
        key_points = self._extract_key_points(text)
        recommendations = []
        
        for point in key_points:
            if "challenge" in point["category"] or "risk" in point["category"]:
                recommendations.append(
                    f"Recommendation: Address {point['point']}"
                )
        
        return recommendations[:5]

    def _split_text(self, text: str, max_length: int = 1024) -> List[str]:
        """Split text into chunks for processing"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_length:
                current_chunk.append(word)
                current_length += len(word) + 1
            else:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = len(word) + 1
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
