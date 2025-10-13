#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import EnhancedChatbot

def test_semantic_model_query():
    chatbot = EnhancedChatbot()
    
    # Test the new Power BI Semantic model query
    test_queries = [
        "I am using the Power BI Semantic model to get some data from other workspace which is not owned by me, where while I published the dashboard in services, the user where I gave access to my dashboard are not able to view the charts which is created by using that Power BI Semantic model",
        "Power BI Semantic model access error from other workspace",
        "Users can't view charts from semantic model in different workspace",
        "Power BI dataset build permissions issue"
    ]
    
    print("Testing Power BI Semantic Model Access Queries:")
    print("=" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query}")
        response = chatbot.get_response(query)
        print(f"   Response: {response}")
        print(f"   Contains Documentation Link: {'learn.microsoft.com' in response}")

if __name__ == "__main__":
    test_semantic_model_query()