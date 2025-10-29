#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import EnhancedChatbot

def test_speed():
    print("Testing Fast Semantic Matcher Speed...")
    chatbot = EnhancedChatbot()
    
    # Test queries
    test_queries = [
        "Why is there a discrepancy between the number shown on screen and the exported data from Power BI?",
        "How can I connect Hive server to Power BI?",
        "Hello how are you?",
        "Users can't see charts from semantic model",
        "What is Python programming language?"
    ]
    
    print(f"\nTesting {len(test_queries)} queries for speed...")
    print("=" * 60)
    
    total_time = 0
    
    for i, query in enumerate(test_queries, 1):
        start_time = time.time()
        
        response, is_trained = chatbot.get_response(query)
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        total_time += response_time
        
        print(f"\n{i}. Query: {query[:50]}{'...' if len(query) > 50 else ''}")
        print(f"   Response Time: {response_time:.1f}ms")
        print(f"   Response: {response[:60]}{'...' if len(response) > 60 else ''}")
        print(f"   From Training: {is_trained}")
    
    avg_time = total_time / len(test_queries)
    print(f"\n" + "=" * 60)
    print(f"PERFORMANCE RESULTS:")
    print(f"Total Time: {total_time:.1f}ms")
    print(f"Average Time per Query: {avg_time:.1f}ms")
    print(f"Queries per Second: {1000/avg_time:.1f}")
    
    if avg_time < 100:
        print("✅ EXCELLENT: Very fast response times!")
    elif avg_time < 500:
        print("✅ GOOD: Acceptable response times")
    else:
        print("⚠️  SLOW: May need further optimization")

if __name__ == "__main__":
    test_speed()