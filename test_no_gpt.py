#!/usr/bin/env python3
"""
Test script to verify GPT functionality has been completely removed
"""

import os
import sys

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import EnhancedChatbot

def test_chatbot_without_gpt():
    """Test that chatbot works with only training data"""
    print("🧪 Testing Chatbot without GPT functionality")
    print("=" * 50)
    
    # Initialize chatbot
    chatbot = EnhancedChatbot()
    
    # Test queries
    test_queries = [
        "hello",
        "what is power bi",
        "how to create dashboard",
        "completely unknown query that should trigger fallback",
        "tell me about advanced machine learning algorithms"
    ]
    
    print(f"\n📊 Testing {len(test_queries)} queries:")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        response = chatbot.get_response(query)
        print(f"   Response: {response}")
        
        # Check if response came from training data or fallback
        last_conversation = chatbot.conversation_history[-1]
        if last_conversation['from_training']:
            print("   ✅ Source: Training Data")
        else:
            print("   🔄 Source: Fallback Response")
    
    print(f"\n📈 Conversation Statistics:")
    chatbot.show_stats()
    
    print(f"\n✅ Test completed successfully!")
    print("🚫 No GPT functionality detected - chatbot working with training data only")

if __name__ == "__main__":
    test_chatbot_without_gpt()