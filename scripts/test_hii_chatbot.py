"""
Test the chatbot with hii greeting in a simple script
"""

import sys
import os

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from chatbot import EnhancedChatbot

def test_hii_chatbot():
    """Test hii with the chatbot"""
    
    chatbot = EnhancedChatbot()
    
    test_inputs = ["hii", "hi", "hello", "what is powerbi"]
    
    print("HII CHATBOT TEST")
    print("=" * 40)
    
    for test_input in test_inputs:
        response = chatbot.get_response(test_input)
        print(f"User: {test_input}")
        print(f"Bot: {response}")
        print("-" * 40)

if __name__ == "__main__":
    test_hii_chatbot()