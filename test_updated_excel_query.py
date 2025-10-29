#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import EnhancedChatbot

def test_updated_excel_query():
    print("Testing updated 30 users Excel connection query...")
    chatbot = EnhancedChatbot()
    
    queries = [
        "Can 30 users have live Excel connections to the same semantic model simultaneously?",
        "Is it safe for 30 users to use live Excel connections to a semantic model simultaneously?",
        "30 users live Excel connections semantic model"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. Query: '{query}'")
        print("-" * 60)
        
        response, is_trained = chatbot.get_response(query)
        
        print(f"Response: {response}")
        print(f"From Training: {is_trained}")
        
        # Check if it contains the expected key phrases from your Amaan Q&A.pdf
        expected_phrases = ["not recommended", "capacity overutilization", "standard excel exports", "strain resources"]
        found_phrases = [phrase for phrase in expected_phrases if phrase.lower() in response.lower()]
        
        print(f"✅ Key phrases found: {found_phrases}")
        
        if "not recommended" in response.lower():
            print("✅ Correct answer from Amaan Q&A.pdf!")
        else:
            print("❌ May not be using the updated answer")

if __name__ == "__main__":
    test_updated_excel_query()