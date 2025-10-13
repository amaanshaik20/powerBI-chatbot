"""
Quick test of greeting variations
"""

import sys
import os

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from chatbot import EnhancedChatbot

def test_greetings():
    """Test greeting variations"""
    
    chatbot = EnhancedChatbot()
    
    greetings = ["hi", "hello", "hey", "hi there", "hello there"]
    
    for greeting in greetings:
        print(f"Q: {greeting}")
        response = chatbot.get_response(greeting)
        print(f"A: {response[:50]}...")
        
        match_info = chatbot.matcher.get_match_info(greeting)
        if match_info:
            print(f"   Match: {match_info['entry']['question']} (Score: {match_info['score']:.3f})")
        print()

if __name__ == "__main__":
    test_greetings()