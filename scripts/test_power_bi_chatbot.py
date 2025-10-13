"""
Test the enhanced chatbot with Power BI questions from the PDF
"""

import sys
import os
import json

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from query_matcher import QueryMatcher

def load_training_data():
    """Load the updated training data"""
    try:
        data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'training_data.json')
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Training data not found!")
        return []

def test_power_bi_questions():
    """Test various Power BI related questions"""
    
    training_data = load_training_data()
    if not training_data:
        print("No training data loaded!")
        return
    
    matcher = QueryMatcher(training_data)
    
    # Test Power BI related questions
    test_questions = [
        # Direct matches from PDF
        "Why is there a discrepancy in Power BI export data?",
        "How to connect Power BI to Azure Databricks?",
        "Power BI scheduled refresh fails",
        "Power BI dataflow running too long",
        "Power BI throttling issues",
        
        # Variations and related questions
        "power bi export problem",
        "databricks connection",
        "refresh error in power bi", 
        "dataflow stuck",
        "gateway issues",
        "jira power bi plugin",
        
        # General questions (should still work)
        "hi there",
        "what is python",
        "thank you",
        
        # Unknown questions (should use fallback)
        "what's the weather like today",
        "how to cook pasta"
    ]
    
    print("POWER BI CHATBOT TEST RESULTS")
    print("=" * 60)
    print(f"Total training entries: {len(training_data)}")
    print(f"Testing {len(test_questions)} questions...\n")
    
    for i, question in enumerate(test_questions, 1):
        response, is_trained = matcher.get_response(question)
        match_info = matcher.get_match_info(question)
        
        print(f"{i:2d}. Question: '{question}'")
        print(f"    Response: {response[:100]}...")
        print(f"    From training: {'✅' if is_trained else '❌'}")
        
        if match_info:
            print(f"    Match score: {match_info['score']:.3f}")
            print(f"    Best match: '{match_info['entry']['question'][:50]}...'")
        
        print("-" * 60)

if __name__ == "__main__":
    test_power_bi_questions()