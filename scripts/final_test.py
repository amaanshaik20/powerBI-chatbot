"""
Final comprehensive test to ensure all question types work correctly
"""

import sys
import os

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from chatbot import EnhancedChatbot

def comprehensive_test():
    """Test various question types to ensure everything works"""
    
    chatbot = EnhancedChatbot()
    
    test_cases = [
        # Power BI definition (should give proper definition now)
        ("what is powerbi", "Should give Power BI definition"),
        
        # Specific Power BI issues (should give specific answers)
        ("power bi refresh fails", "Should give refresh troubleshooting"),
        ("databricks connection", "Should give connection help"),
        
        # General questions (should work normally)  
        ("hi there", "Should greet"),
        ("what is python", "Should define Python"),
        
        # Unrelated questions (should use fallback)
        ("how to add certificate in key store manager", "Should use fallback"),
        ("weather today", "Should use fallback"),
    ]
    
    print("COMPREHENSIVE CHATBOT TEST")
    print("=" * 60)
    print(f"Total training entries: {len(chatbot.training_data)}")
    print()
    
    for question, expected in test_cases:
        print(f"Q: {question}")
        print(f"Expected: {expected}")
        
        response = chatbot.get_response(question)
        match_info = chatbot.matcher.get_match_info(question)
        
        print(f"A: {response[:100]}...")
        
        if match_info:
            print(f"✅ Matched: {match_info['entry']['question'][:40]}... (Score: {match_info['score']:.3f})")
        else:
            print(f"❌ No match - using fallback")
        
        print("-" * 60)

if __name__ == "__main__":
    comprehensive_test()