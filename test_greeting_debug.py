#!/usr/bin/env python3
"""
Test greeting recognition specifically for 'hii'
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import EnhancedChatbot

def test_greeting_variations():
    """Test various greeting formats"""
    chatbot = EnhancedChatbot()
    
    greetings = ['hi', 'hii', 'hiii', 'hello', 'hey', 'Hi', 'HII', 'HELLO']
    
    print("🧪 Testing Greeting Recognition")
    print("=" * 40)
    
    for greeting in greetings:
        response = chatbot.get_response(greeting)
        is_greeting_response = any(word in response.lower() for word in ['hello', 'hi', 'hey', 'good'])
        
        print(f"Input: '{greeting}'")
        print(f"Response: {response}")
        print(f"Status: {'✅ GREETING' if is_greeting_response else '❌ NOT GREETING'}")
        print("-" * 40)

if __name__ == "__main__":
    test_greeting_variations()