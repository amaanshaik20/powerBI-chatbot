"""
Test improved greeting matching with variations
"""

import sys
import os

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from chatbot import EnhancedChatbot

def test_greeting_variations():
    """Test various greeting formats"""
    
    chatbot = EnhancedChatbot()
    
    # Test various greeting variations
    test_greetings = [
        "hi",
        "hii", 
        "hiii",
        "hello",
        "hey",
        "heyyy",
        "hi there",
        "hello there",
        "hey buddy"
    ]
    
    print("GREETING VARIATIONS TEST")
    print("=" * 50)
    
    for greeting in test_greetings:
        print(f"👤 User: {greeting}")
        response = chatbot.get_response(greeting)
        print(f"🤖 Bot: {response[:60]}...")
        
        match_info = chatbot.matcher.get_match_info(greeting)
        if match_info:
            print(f"    ✅ Matched: {match_info['entry']['question']} (Score: {match_info['score']:.3f})")
        else:
            print(f"    ❌ No match - using fallback")
        
        print("-" * 50)

if __name__ == "__main__":
    test_greeting_variations()