"""
Comprehensive test script for all ESG analysis functionalities
"""

import os
from ai.document_processor import DocumentProcessor
from ai.esg_analyzer import ESGAnalyzer
from ai.greenwashing_detector import GreenwashingDetector
from ai.report_summarizer import ReportSummarizer

# Initialize components
doc_processor = DocumentProcessor()
esg_analyzer = ESGAnalyzer()
greenwashing_detector = GreenwashingDetector()
report_summarizer = ReportSummarizer()

# Test data
test_text = """
# Environmental Impact Report

Our company has implemented several initiatives to reduce our carbon footprint:
1. Installed 1000 solar panels across our facilities
2. Reduced water usage by 30% through recycling systems
3. Achieved 50% waste reduction through recycling programs

We are committed to achieving net-zero emissions by 2040.
However, our current progress is slower than expected due to supply chain challenges.
"""

def test_document_processing():
    print("\n=== Testing Document Processing ===")
    # Test with text file
    with open(os.path.join(os.path.dirname(__file__), "test_esg_report.txt"), "r") as f:
        text = f.read()
    print("\nExtracted Text:")
    print(text[:200] + "...")

def test_esg_analysis():
    print("\n=== Testing ESG Analysis ===")
    results = esg_analyzer.analyze_text(test_text)
    
    print("\nESG Scores:")
    for category, score in results["scores"].items():
        print(f"{category}: {score:.2f}")
    
    print("\nKey Topics:")
    for topic in results["key_topics"][:3]:
        print(f"{topic['topic']}: {topic['score']:.2f}")

def test_greenwashing_detection():
    print("\n=== Testing Greenwashing Detection ===")
    results = greenwashing_detector.analyze_text(test_text)
    
    print(f"\nGreenwashing Risk Score: {results['risk_score']:.2f}")
    
    print("\nIndicators:")
    for indicator in results["indicators"]:
        print(f"{indicator['type']}: {indicator['confidence']:.2f}")
    
    print("\nRecommendations:")
    for rec in results["recommendations"]:
        print(f"- {rec}")

def test_report_summarization():
    print("\n=== Testing Report Summarization ===")
    results = report_summarizer.summarize(test_text)
    
    print("\nExecutive Summary:")
    print(results["executive_summary"])
    
    print("\nKey Points:")
    for point in results["key_points"][:3]:
        print(f"- {point['point']}")

if __name__ == "__main__":
    test_document_processing()
    test_esg_analysis()
    test_greenwashing_detection()
    test_report_summarization()
