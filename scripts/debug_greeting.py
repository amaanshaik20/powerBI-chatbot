"""
Debug the 'hi there' greeting issue
"""

import sys
import os
import json

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from query_matcher import QueryMatcher

def debug_greeting():
    """Debug greeting matching"""
    
    # Load training data
    data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'training_data.json')
    with open(data_file, 'r', encoding='utf-8') as f:
        training_data = json.load(f)
    
    matcher = QueryMatcher(training_data)
    
    question = "hi there"
    
    print("GREETING DEBUG")
    print("=" * 40)
    print(f"Question: '{question}'")
    print(f"Threshold: {matcher.min_similarity_threshold}")
    print()
    
    # Find greeting entries
    greeting_entries = []
    for i, entry in enumerate(training_data):
        if any(kw in ['hello', 'hi', 'hey', 'greetings'] for kw in entry['keywords']):
            greeting_entries.append((i, entry))
    
    print("GREETING ENTRIES IN TRAINING DATA:")
    for i, entry in greeting_entries:
        print(f"{i}: {entry['question']} | Keywords: {entry['keywords']}")
    
    print("\nMATCH ANALYSIS:")
    cleaned_query = matcher.clean_text(question)
    
    for i, entry in greeting_entries:
        q_sim = matcher.calculate_similarity(cleaned_query, matcher.clean_text(entry['question']))
        k_score = matcher.keyword_match_score(question, entry['keywords'])
        combined = (q_sim * 0.7) + (k_score * 0.3)
        
        print(f"{entry['question'][:30]}... | Q:{q_sim:.3f} K:{k_score:.3f} Combined:{combined:.3f}")
    
    print(f"\nFINAL RESULT:")
    response, is_trained = matcher.get_response(question)
    print(f"Response: {response[:100]}...")
    print(f"From training: {is_trained}")

if __name__ == "__main__":
    debug_greeting()