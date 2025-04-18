"""
Test script for ESG analysis components
"""

import os
from ai.document_processor import DocumentProcessor
from ai.esg_analyzer import ESGAnalyzer
from ai.greenwashing_detector import GreenwashingDetector
from ai.report_summarizer import ReportSummarizer

def main():
    # Initialize components
    doc_processor = DocumentProcessor()
    esg_analyzer = ESGAnalyzer()
    greenwashing_detector = GreenwashingDetector()
    report_summarizer = ReportSummarizer()
    
    # Read test file
    with open("test_esg_report.txt", "r") as f:
        text = f.read()
    
    print("\n=== ESG Analysis ===")
    esg_results = esg_analyzer.analyze_text(text)
    print("ESG Scores:", esg_results["scores"])
    print("\nKey Topics:", esg_results["key_topics"][:3])
    
    print("\n=== Greenwashing Detection ===")
    greenwashing_results = greenwashing_detector.analyze_text(text)
    print("Risk Score:", greenwashing_results["risk_score"])
    print("\nIndicators:", greenwashing_results["indicators"][:3])
    
    print("\n=== Report Summarization ===")
    summary_results = report_summarizer.summarize(text)
    print("\nExecutive Summary:")
    print(summary_results["executive_summary"])
    print("\nKey Points:", summary_results["key_points"][:3])

if __name__ == "__main__":
    main()
