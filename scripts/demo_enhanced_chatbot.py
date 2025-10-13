"""
Demo script to showcase the enhanced chatbot with Power BI knowledge
"""

import sys
import os

# Add paths for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from chatbot import EnhancedChatbot

def demo_chatbot():
    """Demo the enhanced chatbot with sample questions"""
    
    print("🤖 ENHANCED CHATBOT DEMO - POWER BI KNOWLEDGE")
    print("=" * 60)
    
    # Initialize chatbot
    chatbot = EnhancedChatbot()
    
    # Demo questions covering different areas
    demo_questions = [
        "hi",
        "What causes Power BI throttling?",
        "How to connect to Azure Databricks?",
        "My dataflow is stuck, what should I do?",
        "Why can't I see Create App option?",
        "How to handle timezone in Power BI?",
        "What about weather forecast?",  # Should use fallback
        "thank you"
    ]
    
    print(f"📚 Loaded {len(chatbot.training_data)} training entries")
    print("🔍 Testing various questions...\n")
    
    for i, question in enumerate(demo_questions, 1):
        print(f"👤 User: {question}")
        
        response = chatbot.get_response(question)
        if response == "exit":
            break
            
        print(f"🤖 Bot: {response}")
        
        # Show match info for debugging
        match_info = chatbot.matcher.get_match_info(question)
        if match_info:
            print(f"    💡 Match score: {match_info['score']:.3f}")
        else:
            print(f"    💡 No match found - used fallback")
        
        print("-" * 50)
    
    # Show conversation stats
    print("\n📊 CONVERSATION STATISTICS:")
    chatbot.show_stats()

if __name__ == "__main__":
    demo_chatbot()