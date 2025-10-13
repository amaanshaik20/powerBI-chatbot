"""
Test the chatbot with various greeting inputs to debug matching issues
"""

import sys
import os
import json

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))

from query_matcher import QueryMatcher

def load_training_data():
    """Load the actual training data"""
    try:
        data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'training_data.json')
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Training data not found!")
        return []

def test_greetings():
    """Test various greeting inputs"""
    
    training_data = load_training_data()
    if not training_data:
        print("No training data loaded!")
        return
    
    matcher = QueryMatcher(training_data)
    
    # Test various greeting inputs
    test_inputs = [
        "hi",
        "hii", 
        "hey",
        "hello",
        "hi there",
        "hey there",
        "hello world",
        "greetings",
        "how are you",
        "how are you doing",
        "what is python",
        "unknown query that should fail"
    ]
    
    print("GREETING TEST RESULTS")
    print("=" * 50)
    
    for test_input in test_inputs:
        response, is_trained = matcher.get_response(test_input)
        match_info = matcher.get_match_info(test_input)
        
        print(f"\nInput: '{test_input}'")
        print(f"Response: {response}")
        print(f"From training: {is_trained}")
        
        if match_info:
            print(f"Score: {match_info['score']:.3f}")
            print(f"Best match: '{match_info['entry']['question']}'")
            print(f"Keywords: {match_info['entry']['keywords']}")
        else:
            print("No match found")
        print("-" * 30)

if __name__ == "__main__":
    test_greetings()