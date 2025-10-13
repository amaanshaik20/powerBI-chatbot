#!/usr/bin/env python3

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import EnhancedChatbot

def test_hive_query():
    """Test the specific Hive server to Power BI query"""
    chatbot = EnhancedChatbot()
    
    query = "How can I connect Hive server to Power BI?"
    print(f"🔍 Testing Query: {query}")
    print("=" * 60)
    
    response = chatbot.get_response(query)
    print(f"🤖 Response: {response}")
    print("=" * 60)
    
    # Let's also test the matching process
    from query_matcher import QueryMatcher
    from data.training_data import training_data
    
    matcher = QueryMatcher(training_data)
    
    match = matcher.find_best_match(query)
    if match:
        print(f"📊 Match Details:")
        print(f"   Question: {match['entry']['question']}")
        print(f"   Score: {match['score']:.3f}")
        print(f"   Answer: {match['entry']['answer']}")
    else:
        print("❌ No match found")

if __name__ == "__main__":
    test_hive_query()