#!/usr/bin/env python3
"""
Debug the exact keyword matching issue for 'hii'
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from query_matcher import QueryMatcher
import json

def test_keyword_matching():
    """Test the keyword matching specifically"""
    
    # Load training data
    with open('data/training_data.json', 'r') as f:
        training_data = json.load(f)
    
    matcher = QueryMatcher(training_data)
    
    # Find greeting entry
    greeting_entry = None
    for entry in training_data:
        if 'hello' in entry['keywords'] or 'hi' in entry['keywords']:
            greeting_entry = entry
            break
    
    if not greeting_entry:
        print("❌ No greeting entry found!")
        return
    
    print("🔍 Debugging Keyword Matching for 'hii'")
    print("=" * 50)
    print(f"Greeting Entry Keywords: {greeting_entry['keywords']}")
    print(f"Greeting Entry Answer: {greeting_entry['answer']}")
    print()
    
    test_queries = ['hi', 'hii', 'hiii', 'hello', 'HII']
    
    for query in test_queries:
        print(f"Testing: '{query}'")
        
        # Test individual components
        cleaned_query = matcher.clean_text(query)
        user_words = set(cleaned_query.split())
        
        print(f"  Cleaned query: '{cleaned_query}'")
        print(f"  User words: {user_words}")
        
        # Test keyword matching
        keyword_score = matcher.keyword_match_score(query, greeting_entry['keywords'])
        print(f"  Keyword score: {keyword_score}")
        
        # Test question similarity
        question_similarity = matcher.calculate_similarity(cleaned_query, matcher.clean_text(greeting_entry['question']))
        print(f"  Question similarity: {question_similarity}")
        
        # Combined score
        combined_score = (question_similarity * 0.7) + (keyword_score * 0.3)
        print(f"  Combined score: {combined_score}")
        
        # Test relevance
        is_relevant = matcher.is_relevant_match(query, greeting_entry, combined_score)
        print(f"  Is relevant: {is_relevant}")
        
        # Find best match
        best_match = matcher.find_best_match(query)
        if best_match:
            print(f"  Best match keys: {best_match.keys()}")
            if 'entry' in best_match:
                print(f"  Best match answer: {best_match['entry']['answer'][:50]}...")
            elif 'answer' in best_match:
                print(f"  Best match answer: {best_match['answer'][:50]}...")
            else:
                print(f"  Best match content: {best_match}")
        else:
            print("  No match found")
        
        print("-" * 30)

if __name__ == "__main__":
    test_keyword_matching()