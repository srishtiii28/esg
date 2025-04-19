"""Greenwashing detection module for identifying misleading ESG claims"""

from typing import Dict, List
from transformers import pipeline

class GreenwashingDetector:
    def __init__(self):
        """Initialize the greenwashing detector with necessary models"""
        self.classifier = pipeline(
            "text-classification",
            model="nlptown/bert-base-multilingual-uncased-sentiment"
        )
        
        # Define common greenwashing indicators
        self.indicators = [
            "commitment without action",
            "vague sustainability claims",
            "unsubstantiated environmental benefits",
            "selective disclosure",
            "green marketing",
            "environmental claims without evidence"
        ]

    def analyze_text(self, text: str) -> Dict:
        """Analyze text for greenwashing indicators"""
        results = {
            "risk_score": 0.0,
            "indicators": []
        }

        # Check for each indicator
        for indicator in self.indicators:
            # Check if indicator is present in text
            if indicator in text.lower():
                # Analyze sentiment around the indicator
                context = text[text.lower().find(indicator)-100:text.lower().find(indicator)+100]
                sentiment = self.classifier(context)[0]
                
                # Calculate risk score based on sentiment
                risk_score = 1.0 - (sentiment["score"] / 5)  # Convert 1-5 scale to 0-1
                
                results["indicators"].append({
                    "type": indicator.replace(" ", "_"),
                    "description": indicator,
                    "confidence": float(risk_score),
                    "severity": "high" if risk_score > 0.7 else "medium",
                    "text_snippet": context
                })

        # Calculate overall risk score
        if results["indicators"]:
            scores = [ind["confidence"] for ind in results["indicators"]]
            results["risk_score"] = float(np.mean(scores))

        return results
