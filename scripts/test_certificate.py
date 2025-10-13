"""
Quick test of the certificate question specifically
"""

import sys
import os
import json

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from chatbot import EnhancedChatbot

def test_certificate_question():
    """Test the specific certificate question"""
    
    chatbot = EnhancedChatbot()
    
    questions = [
        "how to add certificate in key store manager",
        "hi there",
        "power bi refresh error",
        "what is python"
    ]
    
    print("CERTIFICATE QUESTION TEST")
    print("=" * 40)
    
    for question in questions:
        response = chatbot.get_response(question)
        match_info = chatbot.matcher.get_match_info(question)
        
        print(f"Q: {question}")
        print(f"A: {response}")
        
        if match_info:
            print(f"   Match: {match_info['entry']['question'][:40]}...")
            print(f"   Score: {match_info['score']:.3f}")
        else:
            print(f"   No match - using fallback")
        print("-" * 40)

if __name__ == "__main__":
    test_certificate_question()