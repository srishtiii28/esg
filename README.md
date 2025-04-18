# GreenStamp

AI + Blockchain-powered ESG Analysis Platform

## Features

### AI-Powered ESG Analysis
- OCR + NLP for content extraction and analysis
- Comprehensive ESG scoring with subcategory analysis
- Advanced greenwashing detection using DeBERTa
- BART-based intelligent report summarization
- Detailed evidence extraction and scoring
- Category-specific analysis for 18+ ESG factors

### Blockchain Integration
- Tamper-proof report hash storage on Polygon
- IPFS-based decentralized document storage
- Instant verification of report authenticity

### User Interface
- Modern, responsive dashboard
- File upload portal
- Interactive ESG score visualization
- Blockchain verification status display
- Searchable and sortable report database

## Tech Stack
- Frontend: Next.js + TypeScript
- Backend: Python FastAPI
- Blockchain: Web3.py + Polygon
- AI: Transformers, PyTesseract
- Storage: IPFS (web3.storage)

## Project Structure
```
greenStamp/
├── frontend/           # Next.js frontend application
├── backend/           # Python FastAPI backend
│   ├── ai/           # AI models and processing
│   ├── blockchain/   # Blockchain integration
│   └── api/          # API endpoints
└── docs/             # Documentation
```

## Getting Started

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/greenStamp.git
cd greenStamp
```

2. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Start the API server:
```bash
uvicorn api.main:app --reload
```

### Using the API

#### Analyzing ESG Reports

```python
import requests

# Upload and analyze an ESG report
url = "http://localhost:8000/analyze"
files = {"file": open("esg_report.pdf", "rb")}
response = requests.post(url, files=files)

# Access the analysis results
result = response.json()

# Overall ESG scores
total_score = result["total"]
environmental_score = result["environmental"]
social_score = result["social"]
governance_score = result["governance"]

# Detailed category analysis
env_categories = result["analysis"]["category_details"]["environmental"]
climate_score = env_categories["subcategories"]["climate_change"]["score"]

# Greenwashing warnings
warnings = result["analysis"]["greenwashing_warnings"]
for warning in warnings:
    print(f"Warning: {warning['type']} - {warning['description']}")
    print(f"Confidence: {warning['confidence']}")

# Report summary
summary = result["analysis"]["summary"]["brief"]
full_summary = result["analysis"]["summary"]["full"]
```

### API Response Structure

```json
{
  "environmental": 75.5,
  "social": 68.2,
  "governance": 82.1,
  "total": 75.3,
  "report_hash": "0x123...",
  "analysis": {
    "scores": {
      "environmental": 75.5,
      "social": 68.2,
      "governance": 82.1,
      "total": 75.3
    },
    "category_details": {
      "environmental": {
        "subcategories": {
          "climate_change": {"score": 82.5},
          "emissions": {"score": 76.3},
          // ... other categories
        }
      },
      // social and governance categories
    },
    "greenwashing_warnings": [
      {
        "type": "vague_claims",
        "description": "Claims without specific metrics",
        "confidence": 0.85,
        "severity": "high",
        "text_snippet": "..."
      }
    ],
    "summary": {
      "brief": "200-character summary...",
      "full": "Complete summary...",
      "length": 1500,
      "compression_ratio": 0.15
    }
  }
}
```

### AI Models Used

1. **ESG Classification**: FinBERT-ESG for primary scoring
2. **Environmental Analysis**: Fine-tuned BERT for environmental sentiment
3. **Greenwashing Detection**: DeBERTa-v3 for pattern recognition
4. **Report Summarization**: BART-large-CNN for intelligent summarization
5. **OCR**: Tesseract for text extraction from PDFs/images
