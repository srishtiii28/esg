"""Greenwashing detection module to identify potential misleading ESG claims"""

from typing import Dict, List
from transformers import pipeline
import numpy as np
from textblob import TextBlob

class GreenwashingDetector:
    def __init__(self):
        """Initialize the greenwashing detector with necessary models"""
        self.fact_checker = pipeline("zero-shot-classification",
                                   model="facebook/bart-large-mnli")
        
        # Common greenwashing indicators
        self.greenwashing_patterns = [
            "vague environmental claims",
            "hidden trade-offs",
            "no proof",
            "false labels",
            "irrelevant claims",
            "lesser of two evils",
            "fibbing",
            "excessive jargon"
        ]
        
        # Specific phrases that might indicate greenwashing
        self.suspicious_phrases = [
            "eco-friendly",
            "green",
            "sustainable",
            "natural",
            "environmentally conscious",
            "carbon neutral",
            "net zero",
            "100% renewable"
        ]

    def analyze_text(self, text: str) -> Dict:
        """Perform comprehensive greenwashing analysis on the text"""
        results = {
            "risk_score": self._calculate_risk_score(text),
            "indicators": self._identify_greenwashing_indicators(text),
            "claims_analysis": self._analyze_environmental_claims(text),
            "recommendations": self._generate_recommendations(text)
        }
        return results

    def _calculate_risk_score(self, text: str) -> float:
        """Calculate overall greenwashing risk score"""
        # Check for pattern matches
        pattern_results = self.fact_checker(text, self.greenwashing_patterns, 
                                          multi_label=True)
        pattern_score = np.mean([score for score in pattern_results['scores']])
        
        # Analyze sentiment and subjectivity
        blob = TextBlob(text)
        subjectivity_score = blob.sentiment.subjectivity
        
        # Count suspicious phrases
        phrase_count = sum(1 for phrase in self.suspicious_phrases 
                         if phrase.lower() in text.lower())
        phrase_score = min(phrase_count / 10, 1.0)  # Normalize to [0,1]
        
        # Combine scores with weights
        final_score = (0.4 * pattern_score + 
                      0.3 * subjectivity_score + 
                      0.3 * phrase_score)
        
        return float(final_score)

    def _identify_greenwashing_indicators(self, text: str) -> List[Dict]:
        """Identify specific greenwashing indicators in the text"""
        indicators = []
        
        # Check each pattern
        results = self.fact_checker(text, self.greenwashing_patterns, 
                                  multi_label=True)
        
        for pattern, score in zip(results['labels'], results['scores']):
            if score > 0.3:  # Only include significant indicators
                indicators.append({
                    "type": pattern,
                    "confidence": float(score),
                    "severity": "high" if score > 0.7 else "medium" if score > 0.5 else "low"
                })
        
        return sorted(indicators, key=lambda x: x['confidence'], reverse=True)

    def _analyze_environmental_claims(self, text: str) -> List[Dict]:
        """Analyze specific environmental claims for credibility"""
        # Split text into sentences
        blob = TextBlob(text)
        claims = []
        
        for sentence in blob.sentences:
            # Check if sentence contains environmental claims
            if any(phrase in sentence.lower() for phrase in self.suspicious_phrases):
                # Analyze claim credibility
                credibility = self.fact_checker(
                    str(sentence),
                    ["specific and measurable", "vague and unsubstantiated"],
                    multi_label=False
                )
                
                claims.append({
                    "claim": str(sentence),
                    "credibility_score": float(credibility['scores'][0]),
                    "classification": "credible" if credibility['scores'][0] > 0.6 else "suspicious"
                })
        
        return claims

    def _generate_recommendations(self, text: str) -> List[str]:
        """Generate recommendations for improving ESG reporting transparency"""
        recommendations = []
        indicators = self._identify_greenwashing_indicators(text)
        
        for indicator in indicators:
            if indicator['type'] == "vague environmental claims":
                recommendations.append("Provide specific, measurable environmental impact data")
            elif indicator['type'] == "no proof":
                recommendations.append("Include verifiable evidence and third-party certifications")
            elif indicator['type'] == "hidden trade-offs":
                recommendations.append("Disclose full environmental impact, including potential negative effects")
            elif indicator['type'] == "excessive jargon":
                recommendations.append("Use clear, simple language to describe environmental initiatives")
        
        return list(set(recommendations))  # Remove duplicates
