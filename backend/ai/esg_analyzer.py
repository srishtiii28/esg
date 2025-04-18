from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from typing import Dict, List, Tuple, Optional
import torch
from transformers import BartForConditionalGeneration, BartTokenizer, T5Tokenizer, T5ForConditionalGeneration

class ESGAnalyzer:
    def __init__(self):
        try:
            # Load sentiment analysis model (public model)
            self.sentiment_classifier = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )
            
            # Load text classification model for ESG (public model)
            self.esg_classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli"
            )
            
            # Load text classification for greenwashing (public model)
            self.greenwashing_classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli"
            )
            
            # Load summarization model (public model)
            self.summarizer = pipeline(
                "summarization",
                model="sshleifer/distilbart-cnn-12-6"
            )
            
            # Initialize scores
            self.scores = {
                'environmental': 0.0,
                'social': 0.0,
                'governance': 0.0,
                'total': 0.0
            }
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize AI models: {str(e)}")
        
        # ESG categories mapping
        self.esg_categories = {
            'environmental': [
                'climate_change',
                'emissions',
                'energy',
                'waste',
                'water',
                'biodiversity'
            ],
            'social': [
                'labor_rights',
                'human_rights',
                'community',
                'health_safety',
                'diversity',
                'data_privacy'
            ],
            'governance': [
                'board_structure',
                'compensation',
                'shareholder_rights',
                'ethics',
                'corruption',
                'transparency'
            ]
        }

    async def analyze_text(self, text: str) -> Dict[str, any]:
        """Analyze text and return ESG scores using zero-shot classification"""
        try:
            if not text or not text.strip():
                raise ValueError("Empty text provided")

            chunks = self._chunk_text(text)
            if not chunks:
                raise ValueError("No text chunks to analyze")

            scores = {
                'environmental': 0.0,
                'social': 0.0,
                'governance': 0.0
            }
            
            esg_categories = [
                "environmental impact and sustainability",
                "social responsibility and community impact",
                "corporate governance and ethics"
            ]
            
            chunk_scores = []
            for chunk in chunks:
                try:
                    # Use zero-shot classification for ESG scoring
                    results = self.esg_classifier(
                        chunk,
                        candidate_labels=esg_categories,
                        multi_label=True
                    )
                    
                    # Get sentiment
                    sentiment = self.sentiment_classifier(chunk)[0]
                    sentiment_score = 1.0 if sentiment['label'] == 'POSITIVE' else 0.0
                    
                    # Store chunk scores
                    chunk_scores.append({
                        'environmental': float(results['scores'][0] * (0.7 + 0.3 * sentiment_score)),
                        'social': float(results['scores'][1] * (0.7 + 0.3 * sentiment_score)),
                        'governance': float(results['scores'][2] * (0.7 + 0.3 * sentiment_score))
                    })
                except Exception as e:
                    print(f"Warning: Error processing chunk: {str(e)}")
                    continue
            
            if not chunk_scores:
                raise ValueError("Failed to analyze any text chunks")
            
            # Calculate final scores
            for key in scores:
                try:
                    scores[key] = sum(float(chunk[key]) for chunk in chunk_scores) / len(chunk_scores)
                    scores[key] = min(max(scores[key], 0.0), 1.0)  # Ensure score is between 0 and 1
                except:
                    scores[key] = 0.0
            
            # Calculate total score
            try:
                scores['total'] = sum(float(scores[key]) for key in ['environmental', 'social', 'governance']) / 3.0
            except:
                scores['total'] = 0.0
            
            # Store scores
            self.scores = scores.copy()
            
            try:
                # Add detailed category analysis
                category_details = await self._analyze_categories(text)
                scores['category_details'] = {
                    'environmental': {},
                    'social': {},
                    'governance': {}
                }
                for category in ['environmental', 'social', 'governance']:
                    if category in category_details:
                        scores['category_details'][category] = {
                            k: min(max(float(v), 0.0), 1.0)
                            for k, v in category_details[category].items()
                        }
            except Exception as e:
                print(f"Warning: Error in category analysis: {str(e)}")
                scores['category_details'] = {
                    'environmental': {},
                    'social': {},
                    'governance': {}
                }
            
            try:
                # Generate summary
                summary = await self.generate_summary(text)
                scores['summary'] = {
                    'brief': str(summary.get('brief', 'Error generating summary')),
                    'full': str(summary.get('full', 'Error generating summary')),
                    'length': int(summary.get('length', len(text))),
                    'compression_ratio': float(summary.get('compression_ratio', 1.0))
                }
            except Exception as e:
                print(f"Warning: Error generating summary: {str(e)}")
                scores['summary'] = {
                    'brief': 'Error generating summary',
                    'full': 'Error generating summary',
                    'length': len(text),
                    'compression_ratio': 1.0
                }
            
            return scores
        except Exception as e:
            raise ValueError(f"Error analyzing text: {str(e)}")

    async def detect_greenwashing(self, text: str) -> List[Dict]:
        """Detect potential greenwashing in the text"""
        chunks = self._chunk_text(text, chunk_size=256)
        warnings = []

        greenwashing_indicators = [
            "vague environmental claims",
            "misleading statistics",
            "hidden trade-offs",
            "false certifications",
            "irrelevant claims"
        ]

        for chunk in chunks:
            try:
                results = self.greenwashing_classifier(
                    chunk,
                    candidate_labels=greenwashing_indicators,
                    multi_label=True
                )
                
                for label, score in zip(results['labels'], results['scores']):
                    if score > 0.6:  # Confidence threshold
                        warnings.append({
                            'type': label,
                            'description': f'Potential {label} detected',
                            'confidence': float(score),
                            'severity': 'high' if score > 0.8 else 'medium',
                            'text_snippet': chunk[:200] + '...' if len(chunk) > 200 else chunk
                        })
            except Exception as e:
                print(f"Warning: Error detecting greenwashing: {str(e)}")
                continue
        
        # Add contextual warnings based on ESG scores
        if self.scores['environmental'] > 0.9 and len(warnings) > 2:
            warnings.append({
                'type': 'high_score_suspicious',
                'description': 'Unusually high environmental score with multiple greenwashing indicators',
                'confidence': 0.85,
                'severity': 'high'
            })
        
        return warnings

    def _chunk_text(self, text: str, chunk_size: int = 512) -> List[str]:
        """Split text into manageable chunks for analysis"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
        
        return chunks

    async def _analyze_categories(self, text: str) -> Dict[str, Dict[str, float]]:
        """Analyze text for specific ESG categories"""
        try:
            chunks = self._chunk_text(text, chunk_size=256)  # Smaller chunks for detailed analysis
            if not chunks:
                return {}

            category_scores = {}
            
            # Analyze each chunk for category-specific keywords and context
            for category, subcategories in self.esg_categories.items():
                category_scores[category] = {}
                for subcategory in subcategories:
                    try:
                        # Use zero-shot classification for each subcategory
                        results = self.esg_classifier(
                            text[:1000],  # Use first 1000 chars for efficiency
                            candidate_labels=[subcategory.replace('_', ' ')],
                            multi_label=False
                        )
                        category_scores[category][subcategory] = float(results['scores'][0])
                    except Exception as e:
                        print(f"Warning: Error analyzing subcategory {subcategory}: {str(e)}")
                        category_scores[category][subcategory] = 0.0
            
            return category_scores
        except Exception as e:
            print(f"Warning: Error in category analysis: {str(e)}")
            return {}

    async def generate_summary(self, text: str) -> Dict[str, any]:
        """Generate a summary of the ESG report"""
        chunks = self._chunk_text(text, chunk_size=1024)
        summaries = []

        try:
            for chunk in chunks:
                summary = self.summarizer(
                    chunk,
                    max_length=150,
                    min_length=40,
                    do_sample=False
                )[0]['summary_text']
                summaries.append(summary)

            # Combine summaries
            full_summary = ' '.join(summaries)
            
            # Generate brief summary
            brief_summary = self.summarizer(
                full_summary,
                max_length=100,
                min_length=30,
                do_sample=False
            )[0]['summary_text']

            return {
                'brief': brief_summary,
                'full': full_summary,
                'length': len(full_summary),
                'compression_ratio': len(full_summary) / len(text)
            }
        except Exception as e:
            print(f"Warning: Error generating summary: {str(e)}")
            return {
                'brief': 'Error generating summary',
                'full': 'Error generating summary',
                'length': 0,
                'compression_ratio': 0
            }
