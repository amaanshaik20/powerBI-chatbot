#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import EnhancedChatbot

def test_excel_connection_query():
    print("Testing 30 users Excel connection query...")
    chatbot = EnhancedChatbot()
    
    query = "Is it safe for 30 users to use live Excel connections to a semantic model simultaneously?"
    
    print(f"Query: '{query}'")
    print("-" * 80)
    
    response, is_trained = chatbot.get_response(query)
    match_info = chatbot.matcher.get_match_info(query)
    
    print(f"Response: {response}")
    print(f"From Training Data: {is_trained}")
    
    if match_info:
        print(f"\nMatch Details:")
        print(f"  Score: {match_info['score']:.3f}")
        print(f"  Matched Question: '{match_info['entry']['question']}'")
        print(f"  Intent: {match_info['intent']}")
        if 'technology_penalty' in match_info:
            print(f"  Technology Penalty: {match_info['technology_penalty']:.3f}")
    
    print(f"\nExpected Answer from Training Data:")
    print("'Live connections should be evaluated for capacity impact. Consider the semantic model's capacity and potential performance implications with multiple concurrent users.'")

if __name__ == "__main__":
    test_excel_connection_query()