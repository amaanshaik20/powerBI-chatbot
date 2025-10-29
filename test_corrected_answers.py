#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import EnhancedChatbot

def test_corrected_answers():
    """Test key questions to ensure they match Amaan Q&A.pdf answers"""
    
    print("Testing Corrected Training Data from Amaan Q&A.pdf")
    print("=" * 60)
    
    chatbot = EnhancedChatbot()
    
    # Key test cases from the PDF
    test_cases = [
        {
            "query": "Why is there a discrepancy between the number shown on screen and the exported data from Power BI?",
            "expected_keywords": ["attributes", "visualization", "unsafe", "static"],
            "should_not_contain": ["filters", "aggregation methods"]
        },
        {
            "query": "Is it safe for 30 users to use live Excel connections to a semantic model simultaneously?",
            "expected_keywords": ["not recommended", "overutilization", "strain resources"],
            "should_not_contain": ["should be evaluated"]
        },
        {
            "query": "How can I connect Power BI Server to Azure Databricks?",
            "expected_keywords": ["azure databricks", "colo-1", "sharepoint"],
            "should_not_contain": ["cloudera", "drivers"]
        },
        {
            "query": "Why did my Sales Cockpit report fail to refresh?",
            "expected_keywords": ["gateway", "version update", "retrying"],
            "should_not_contain": ["delayed"]
        },
        {
            "query": "How can I connect Hive server to Power BI?",
            "expected_keywords": ["cloudera", "drivers", "tls"],
            "should_not_contain": ["azure", "databricks"]
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test['query'][:50]}...")
        print("-" * 50)
        
        response, is_trained = chatbot.get_response(test['query'])
        
        print(f"Response: {response}")
        print(f"From Training: {is_trained}")
        
        # Check expected keywords
        response_lower = response.lower()
        found_expected = [kw for kw in test['expected_keywords'] if kw.lower() in response_lower]
        found_unwanted = [kw for kw in test['should_not_contain'] if kw.lower() in response_lower]
        
        print(f"✅ Expected found: {found_expected}")
        if found_unwanted:
            print(f"❌ Unwanted found: {found_unwanted}")
        else:
            print("✅ No unwanted keywords")
        
        if len(found_expected) >= 2 and not found_unwanted:
            print("🎯 CORRECT - Matches PDF answer!")
        else:
            print("⚠️  May need review")

if __name__ == "__main__":
    test_corrected_answers()