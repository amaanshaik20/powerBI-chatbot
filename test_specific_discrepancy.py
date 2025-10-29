#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import EnhancedChatbot

def test_specific_query():
    print("Testing specific query with semantic understanding...")
    chatbot = EnhancedChatbot()
    
    # Test the exact query from user
    query = "Why is there a discrepancy between the number shown on screen and the exported data from Power BI?"
    
    print(f"\nQuery: '{query}'")
    print("-" * 80)
    
    # Get response
    response, is_trained = chatbot.get_response(query)
    
    print(f"Response: {response}")
    print(f"From Training Data: {is_trained}")
    
    # Get detailed match info
    match_info = chatbot.matcher.get_match_info(query)
    
    if match_info:
        print(f"\n🔍 Match Details:")
        print(f"Overall Score: {match_info['score']:.3f}")
        print(f"Intent: {match_info['query_intent']['intent']}")
        print(f"Detected Entities: {match_info['query_intent']['entities']}")
        print(f"Matched Training Entry: '{match_info['entry']['question']}'")
        
        print(f"\n📊 Score Breakdown:")
        print(f"  - Question Similarity: {match_info['question_similarity']:.3f}")
        print(f"  - Keyword Similarity: {match_info['keyword_similarity']:.3f}")
        print(f"  - Semantic Similarity: {match_info['semantic_similarity']:.3f}")
        print(f"  - Intent Similarity: {match_info['intent_similarity']:.3f}")
        
        print(f"\n🎯 Expected Training Entry:")
        print(f"Question: 'Why is there a discrepancy when exporting data from Power BI to CSV?'")
        print(f"Answer: 'Data discrepancies can occur due to visualization filters, data type conversions, or different aggregation methods between the visual and export. Check your filters and data model.'")
        
    else:
        print("❌ No match found - using fallback response")
        
        # Let's check all training entries for Power BI discrepancy
        print("\n🔍 Checking for related training entries...")
        for i, entry in enumerate(chatbot.training_data):
            if 'discrepancy' in entry['question'].lower() or 'discrepancy' in ' '.join(entry['keywords']).lower():
                print(f"Found related entry #{i}: {entry['question']}")
                print(f"Keywords: {entry['keywords']}")

if __name__ == "__main__":
    test_specific_query()