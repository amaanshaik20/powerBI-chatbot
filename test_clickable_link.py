#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import EnhancedChatbot

def test_clickable_link():
    chatbot = EnhancedChatbot()
    
    # Test the Power BI Semantic model query with clickable link
    query = "I am using the Power BI Semantic model to get some data from other workspace which is not owned by me, where while I published the dashboard in services, the user where I gave access to my dashboard are not able to view the charts which is created by using that Power BI Semantic model"
    
    print("Testing Power BI Semantic Model Query with Clickable Link:")
    print("=" * 65)
    print(f"\nQuery: {query}")
    
    response = chatbot.get_response(query)
    print(f"\nResponse: {response}")
    
    # Check if the response contains HTML link
    has_html_link = '<a href=' in response and 'target=' in response
    print(f"\nContains Clickable HTML Link: {has_html_link}")
    
    if has_html_link:
        print("✅ SUCCESS: URL is now formatted as a clickable link!")
    else:
        print("❌ ISSUE: URL is not formatted as a clickable link")

if __name__ == "__main__":
    test_clickable_link()