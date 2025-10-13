"""
Test the fixed Power BI question in chatbot
"""

import sys
import os

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from chatbot import EnhancedChatbot

def test_powerbi_chatbot():
    """Test the Power BI question with the chatbot"""
    
    chatbot = EnhancedChatbot()
    
    test_questions = [
        "what is powerbi",
        "what is power bi", 
        "tell me about power bi",
        "power bi definition",
        "what does power bi do"
    ]
    
    print("POWER BI QUESTION TESTS")
    print("=" * 50)
    
    for question in test_questions:
        print(f"Q: {question}")
        response = chatbot.get_response(question)
        print(f"A: {response}")
        
        match_info = chatbot.matcher.get_match_info(question)
        if match_info:
            print(f"   Match: {match_info['entry']['question']}")
            print(f"   Score: {match_info['score']:.3f}")
        print("-" * 50)

if __name__ == "__main__":
    test_powerbi_chatbot()