"""ESG Analysis module for scoring and analyzing ESG reports"""

from typing import Dict, List, Tuple
from transformers import pipeline
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class ESGAnalyzer:
    def __init__(self):
        """Initialize the ESG analyzer with necessary models"""
        self.classifier = pipeline("zero-shot-classification",
                                 model="facebook/bart-large-mnli")
        self.sentiment_analyzer = pipeline("sentiment-analysis",
                                         model="ProsusAI/finbert")
        
        # ESG categories and their respective keywords
        self.esg_categories = {
            "environmental": [
                "climate change", "carbon emissions", "renewable energy",
                "waste management", "water usage", "biodiversity"
            ],
            "social": [
                "employee welfare", "human rights", "community relations",
                "health and safety", "diversity", "inclusion"
            ],
            "governance": [
                "board diversity", "executive compensation", "shareholder rights",
                "business ethics", "corruption", "transparency"
            ]
        }

    def analyze_text(self, text: str) -> Dict:
        """Perform comprehensive ESG analysis on the text"""
        results = {
            "scores": self._calculate_esg_scores(text),
            "sentiment": self._analyze_sentiment(text),
            "key_topics": self._extract_key_topics(text)
        }
        return results

    def _calculate_esg_scores(self, text: str) -> Dict[str, float]:
        """Calculate individual E, S, and G scores"""
        scores = {}
        
        for category, keywords in self.esg_categories.items():
            # Use zero-shot classification to determine relevance to each category
            result = self.classifier(text, keywords, multi_label=True)
            category_score = np.mean([score for score in result['scores']])
            scores[category] = float(category_score)

        # Normalize scores
        scaler = MinMaxScaler()
        normalized_scores = scaler.fit_transform([[v] for v in scores.values()])
        
        return {
            "environmental": float(normalized_scores[0][0]),
            "social": float(normalized_scores[1][0]),
            "governance": float(normalized_scores[2][0]),
            "overall": float(np.mean(normalized_scores))
        }

    def _analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of ESG-related statements"""
        chunks = [text[i:i+512] for i in range(0, len(text), 512)]
        sentiments = []
        
        for chunk in chunks:
            result = self.sentiment_analyzer(chunk)
            sentiments.append(result[0])
        
        # Calculate average sentiment
        avg_sentiment = np.mean([1 if s['label'] == 'positive' else -1 
                               for s in sentiments])
        
        return {
            "score": float(avg_sentiment),
            "label": "positive" if avg_sentiment > 0 else "negative"
        }

    def _extract_key_topics(self, text: str) -> List[Dict]:
        """Extract key ESG topics from the text"""
        all_topics = []
        for category, keywords in self.esg_categories.items():
            result = self.classifier(text, keywords, multi_label=True)
            topics = [{"topic": kw, "score": float(score)} 
                     for kw, score in zip(result['labels'], result['scores'])
                     if score > 0.3]  # Only include relevant topics
            all_topics.extend(topics)
        
        # Sort by relevance score
        all_topics.sort(key=lambda x: x['score'], reverse=True)
        return all_topics[:10]  # Return top 10 topics
