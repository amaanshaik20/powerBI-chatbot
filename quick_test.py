#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import EnhancedChatbot

def quick_test():
    chatbot = EnhancedChatbot()
    
    query = "Why is there a discrepancy between the number shown on screen and the exported data from Power BI?"
    
    print(f"Query: {query}")
    response, is_trained = chatbot.get_response(query)
    print(f"Response: {response}")
    print(f"From Training: {is_trained}")

if __name__ == "__main__":
    quick_test()