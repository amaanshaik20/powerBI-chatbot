#!/usr/bin/env python3
"""
Test script to check AI vs Power BI matching
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import EnhancedChatbot

def test_ai_vs_powerbi():
    """Test AI and Power BI queries to ensure they don't cross-match"""
    chatbot = EnhancedChatbot()
    
    test_queries = [
        "what is ai",
        "what is AI", 
        "tell me about AI",
        "what is artificial intelligence",
        "what is power bi",
        "what is Power BI",
        "tell me about power bi"
    ]
    
    print("🧪 Testing AI vs Power BI Query Matching")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\n❓ Query: '{query}'")
        response = chatbot.get_response(query)
        
        # Check if response is about the right topic
        is_ai_query = any(term in query.lower() for term in ['ai', 'artificial intelligence'])
        is_powerbi_query = any(term in query.lower() for term in ['power bi', 'powerbi'])
        
        response_mentions_ai = any(term in response.lower() for term in ['artificial intelligence', ' ai ', 'machine learning'])
        response_mentions_powerbi = any(term in response.lower() for term in ['power bi', 'business intelligence', 'microsoft', 'dashboard'])
        
        print(f"🤖 Response: {response}")
        
        # Validate correct matching
        if is_ai_query and response_mentions_ai:
            print("✅ CORRECT: AI query got AI response")
        elif is_powerbi_query and response_mentions_powerbi:
            print("✅ CORRECT: Power BI query got Power BI response")
        elif is_ai_query and response_mentions_powerbi:
            print("❌ ERROR: AI query got Power BI response!")
        elif is_powerbi_query and response_mentions_ai:
            print("❌ ERROR: Power BI query got AI response!")
        else:
            print("ℹ️  Other/Fallback response")

if __name__ == "__main__":
    test_ai_vs_powerbi()