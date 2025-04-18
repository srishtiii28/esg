"""
Script to download all necessary Hugging Face models
"""

from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers import VisionEncoderDecoderModel, TrOCRProcessor
from transformers import AutoModelForSeq2SeqLM
from transformers import pipeline
import os

# Set up model paths
os.environ['HUGGINGFACE_HUB_CACHE'] = os.path.join(os.path.dirname(__file__), 'models')

# Download models
print("\n=== Downloading ESG Analysis Models ===")
print("Downloading BART for zero-shot classification...")
zero_shot = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

print("\nDownloading FinBERT for sentiment analysis...")
sentiment = pipeline("sentiment-analysis", model="ProsusAI/finbert")

print("\n=== Downloading Greenwashing Detection Models ===")
print("Downloading BART for greenwashing detection...")
greenwashing = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

print("\n=== Downloading Report Summarization Models ===")
print("Downloading BART for summarization...")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

print("\n=== Downloading OCR Models ===")
print("Downloading TrOCR for OCR...")
processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')

print("\nAll models have been successfully downloaded!")
