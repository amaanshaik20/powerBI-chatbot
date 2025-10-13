"""
Test improved fallback detection for unrelated questions
"""

import sys
import os
import json

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from query_matcher import QueryMatcher

def load_training_data():
    """Load the training data"""
    try:
        data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'training_data.json')
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Training data not found!")
        return []

def test_fallback_detection():
    """Test fallback detection for unrelated questions"""
    
    training_data = load_training_data()
    if not training_data:
        print("No training data loaded!")
        return
    
    matcher = QueryMatcher(training_data)
    
    # Test questions that should use fallback
    unrelated_questions = [
        "how to add certificate in key store manager",
        "what's the weather today",
        "how to cook pasta",
        "install nodejs on windows", 
        "create docker container",
        "java spring boot tutorial",
        "machine learning algorithms",
        "cryptocurrency prices",
        "travel to Japan",
        "best pizza recipe"
    ]
    
    # Test questions that should match training data
    related_questions = [
        "hi there",
        "power bi refresh error",
        "what is python",
        "how are you",
        "databricks connection"
    ]
    
    print("FALLBACK DETECTION TEST")
    print("=" * 50)
    print(f"Threshold: {matcher.min_similarity_threshold}")
    print()
    
    print("🔍 UNRELATED QUESTIONS (should use fallback):")
    print("-" * 50)
    
    for question in unrelated_questions:
        response, is_trained = matcher.get_response(question)
        match_info = matcher.get_match_info(question)
        
        status = "✅ FALLBACK" if not is_trained else "❌ MATCHED"
        score = match_info['score'] if match_info else 0.0
        
        print(f"{status} | {score:.3f} | {question}")
        if is_trained and match_info:
            print(f"      Matched: '{match_info['entry']['question'][:40]}...'")
    
    print(f"\n🎯 RELATED QUESTIONS (should match training):")
    print("-" * 50)
    
    for question in related_questions:
        response, is_trained = matcher.get_response(question)
        match_info = matcher.get_match_info(question)
        
        status = "✅ MATCHED" if is_trained else "❌ FALLBACK"
        score = match_info['score'] if match_info else 0.0
        
        print(f"{status} | {score:.3f} | {question}")
        if is_trained and match_info:
            print(f"      Matched: '{match_info['entry']['question'][:40]}...'")

if __name__ == "__main__":
    test_fallback_detection()