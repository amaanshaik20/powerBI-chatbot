#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import EnhancedChatbot

def test_semantic_understanding():
    print("Initializing Enhanced Chatbot with Semantic Understanding...")
    chatbot = EnhancedChatbot()
    
    # Test queries that show semantic understanding vs keyword matching
    test_scenarios = [
        {
            "category": "Same meaning, different words",
            "queries": [
                "How can I connect Hive server to Power BI?",
                "What's the way to link Hive with PowerBI?",
                "Steps to integrate Hive database with Power BI",
                "Connect Power BI to Hive server"
            ]
        },
        {
            "category": "Power BI access issues - semantic variations",
            "queries": [
                "Users can't see charts from shared semantic model",
                "People unable to view dashboard from other workspace",
                "Charts not visible when using external semantic model",
                "Access denied for Power BI semantic model from different workspace"
            ]
        },
        {
            "category": "Greeting variations",
            "queries": [
                "hi",
                "hii",
                "hello there",
                "good morning",
                "hey buddy"
            ]
        },
        {
            "category": "Unrelated queries (should get fallback)",
            "queries": [
                "What's the weather today?",
                "How to cook pasta?",
                "Tell me about quantum physics"
            ]
        }
    ]
    
    print("\n" + "="*70)
    print("SEMANTIC UNDERSTANDING TEST RESULTS")
    print("="*70)
    
    for scenario in test_scenarios:
        print(f"\n🔍 {scenario['category'].upper()}")
        print("-" * 50)
        
        for query in scenario['queries']:
            print(f"\nQuery: '{query}'")
            
            # Get response
            response, is_trained = chatbot.get_response(query)
            
            # Get detailed match info
            match_info = chatbot.matcher.get_match_info(query)
            
            print(f"Response: {response[:100]}{'...' if len(response) > 100 else ''}")
            print(f"From Training: {is_trained}")
            
            if match_info:
                print(f"Match Score: {match_info['score']:.3f}")
                print(f"Intent: {match_info['query_intent']['intent']}")
                print(f"Detected Entities: {match_info['query_intent']['entities']}")
                
                # Show score breakdown
                scores = [
                    f"Question: {match_info['question_similarity']:.2f}",
                    f"Keywords: {match_info['keyword_similarity']:.2f}",
                    f"Semantic: {match_info['semantic_similarity']:.2f}",
                    f"Intent: {match_info['intent_similarity']:.2f}"
                ]
                print(f"Score Breakdown: {' | '.join(scores)}")
            else:
                print("No match found (using fallback)")
    
    print("\n" + "="*70)
    print("TEST COMPLETE - Semantic understanding vs keyword matching comparison")
    print("="*70)

if __name__ == "__main__":
    test_semantic_understanding()