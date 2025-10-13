#!/usr/bin/env python3

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_fresh_hive_query():
    """Test the Hive query with fresh imports"""
    
    # Import fresh training data
    from data.training_data import training_data
    print(f"✅ Loaded {len(training_data)} training entries")
    
    # Check if our new entry is there
    hive_entries = [entry for entry in training_data if 'hive' in entry['question'].lower()]
    print(f"📊 Found {len(hive_entries)} Hive-related entries:")
    for i, entry in enumerate(hive_entries, 1):
        print(f"   {i}. {entry['question']}")
    
    print("\n" + "="*60)
    
    # Create fresh chatbot instance
    from chatbot import EnhancedChatbot
    chatbot = EnhancedChatbot()
    
    query = "How can I connect Hive server to Power BI?"
    print(f"🔍 Testing Query: {query}")
    print("=" * 60)
    
    response = chatbot.get_response(query)
    print(f"🤖 Response: {response}")

if __name__ == "__main__":
    test_fresh_hive_query()