#!/usr/bin/env python3

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import EnhancedChatbot

def test_hive_variations():
    """Test various Hive server related queries"""
    chatbot = EnhancedChatbot()
    
    test_queries = [
        "How can I connect Hive server to Power BI?",
        "Connect Hive to Power BI",
        "Hive server Power BI connection",
        "How to connect Hive with PowerBI?",
        "Power BI Hive integration",
        "How do I resolve Hive Server connection issues?"
    ]
    
    print("🧪 Testing Hive-related Query Variations")
    print("=" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query}")
        print("-" * 50)
        response = chatbot.get_response(query)
        print(f"Response: {response}")
        print()

if __name__ == "__main__":
    test_hive_variations()