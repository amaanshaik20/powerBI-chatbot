#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import EnhancedChatbot

def test_technology_distinction():
    print("Testing Technology-Specific Query Matching...")
    chatbot = EnhancedChatbot()
    
    test_cases = [
        {
            "query": "How can I connect Hive server to Power BI?",
            "expected_keywords": ["cloudera", "drivers", "tls"],
            "should_not_contain": ["azure", "databricks", "colo-1"]
        },
        {
            "query": "How do I connect Power BI Server to Azure Databricks?",
            "expected_keywords": ["azure", "databricks", "colo-1", "gateway"],
            "should_not_contain": ["cloudera", "drivers", "tls"]
        },
        {
            "query": "Connect Power BI to Hive database",
            "expected_keywords": ["cloudera", "drivers"],
            "should_not_contain": ["azure", "databricks"]
        }
    ]
    
    print("=" * 70)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing Query: '{test_case['query']}'")
        print("-" * 50)
        
        response, is_trained = chatbot.get_response(test_case['query'])
        match_info = chatbot.matcher.get_match_info(test_case['query'])
        
        print(f"Response: {response}")
        print(f"From Training: {is_trained}")
        
        if match_info:
            print(f"Match Score: {match_info['score']:.3f}")
            if 'technology_penalty' in match_info:
                print(f"Technology Penalty: {match_info['technology_penalty']:.3f}")
            print(f"Matched Question: '{match_info['entry']['question']}'")
        
        # Check if response contains expected keywords
        response_lower = response.lower()
        expected_found = [kw for kw in test_case['expected_keywords'] if kw.lower() in response_lower]
        should_not_found = [kw for kw in test_case['should_not_contain'] if kw.lower() in response_lower]
        
        print(f"\n✅ Expected keywords found: {expected_found}")
        if should_not_found:
            print(f"❌ Unwanted keywords found: {should_not_found}")
            print("⚠️  This indicates incorrect matching!")
        else:
            print("✅ No unwanted keywords found")
        
        print("\n" + "=" * 70)

if __name__ == "__main__":
    test_technology_distinction()