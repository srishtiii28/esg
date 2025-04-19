"""ESG analysis module for scoring and categorizing ESG content"""

from typing import Dict, List, Any
import numpy as np
import os
from transformers import pipeline
from typing import Dict, List, Any
import re
from dotenv import load_dotenv

load_dotenv()

class ESGAnalyzer:
    def __init__(self):
        # Load environment variables
        self.hf_api_key = os.getenv('HUGGINGFACE_API_KEY')
        
        # Load specific models for ESG analysis
        self.environmental_analyzer = pipeline(
            "text-classification",
            model="roberta-base",
            return_all_scores=True,
            model_kwargs={"cache_dir": "./models/environmental"}
        )
        
        self.social_analyzer = pipeline(
            "text-classification",
            model="roberta-base",
            return_all_scores=True,
            model_kwargs={"cache_dir": "./models/social"}
        )
        
        self.governance_analyzer = pipeline(
            "text-classification",
            model="roberta-base",
            return_all_scores=True,
            model_kwargs={"cache_dir": "./models/governance"}
        )
        
        # Create models directory if it doesn't exist
        os.makedirs("./models", exist_ok=True)

    def analyze_text(self, text: str) -> Dict[str, Any]:
        try:
            # Preprocess text
            processed_text = self._preprocess_text(text)

            # Analyze each category
            env_results = self.environmental_analyzer(processed_text)[0]
            soc_results = self.social_analyzer(processed_text)[0]
            gov_results = self.governance_analyzer(processed_text)[0]

            # Calculate scores
            env_score = self._calculate_score(env_results)
            soc_score = self._calculate_score(soc_results)
            gov_score = self._calculate_score(gov_results)

            # Calculate total score
            total_score = (env_score + soc_score + gov_score) / 3

            # Generate category details
            category_details = {
                "environmental": {
                    "score": env_score,
                    "keywords": self._extract_keywords(processed_text, "environmental"),
                    "confidence": env_results
                },
                "social": {
                    "score": soc_score,
                    "keywords": self._extract_keywords(processed_text, "social"),
                    "confidence": soc_results
                },
                "governance": {
                    "score": gov_score,
                    "keywords": self._extract_keywords(processed_text, "governance"),
                    "confidence": gov_results
                }
            }

            return {
                "scores": {
                    "environmental": env_score,
                    "social": soc_score,
                    "governance": gov_score,
                    "total": total_score
                },
                "category_details": category_details
            }
            
        except Exception as e:
            print(f"Error in analysis: {str(e)}")
            raise

    def _preprocess_text(self, text: str) -> str:
        # Basic preprocessing
        text = text.lower()
        text = re.sub(r'\W+', ' ', text)
        text = text.strip()
        return text

    def _calculate_score(self, results: List[Dict[str, Any]]) -> float:
        # Calculate score based on model predictions
        # For now, we'll use the positive score as our metric
        # In a real implementation, we would use a more sophisticated scoring system
        positive_score = next((r["score"] for r in results if r["label"] == "LABEL_1"), 0.5)
        return round(positive_score * 100, 2)

    def _extract_keywords(self, text: str, category: str) -> List[str]:
        # Extract relevant keywords for category
        keywords = []
        
        # Add category-specific keywords
        if category == "environmental":
            keywords.extend([
                "sustainability",
                "climate change",
                "carbon emissions",
                "greenhouse gases",
                "renewable energy",
                "water usage"
            ])
        elif category == "social":
            keywords.extend([
                "diversity",
                "inclusion",
                "human rights",
                "labor practices",
                "community engagement",
                "employee welfare"
            ])
        elif category == "governance":
            keywords.extend([
                "corporate governance",
                "board composition",
                "executive compensation",
                "risk management",
                "compliance",
                "transparency"
            ])
        
        # Filter keywords present in text
        text_words = set(text.lower().split())
        return [k for k in keywords if k.lower() in text_words]
            max_score = max(classification["scores"])
            max_index = classification["scores"].index(max_score)
            
            # Set the category score
            results["scores"][category] = float(max_score)
            
            # Store subcategory details
            results["category_details"][category] = {
                subcategories[max_index]: float(max_score)
            }

        # Calculate total score
        scores = results["scores"].values()
        results["scores"]["total"] = float(sum(scores) / len(scores))

        return results
