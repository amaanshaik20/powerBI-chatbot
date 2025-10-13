"""
Debug the keyword matching to understand why 'hi' is not matching
"""

import sys
import os
import json

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from query_matcher import QueryMatcher

# Test with simple data
test_data = [
    {
        "question": "hello",
        "answer": "Hello! How can I help you today?",
        "keywords": ["hello", "hi", "hey", "greetings"]
    }
]

matcher = QueryMatcher(test_data)

# Debug specific cases
test_cases = ["hi", "hii", "hey", "hello"]

print("DETAILED KEYWORD MATCHING DEBUG")
print("=" * 40)

for test_input in test_cases:
    print(f"\nTesting: '{test_input}'")
    
    cleaned_query = matcher.clean_text(test_input)
    print(f"Cleaned query: '{cleaned_query}'")
    
    user_words = set(cleaned_query.split())
    print(f"User words: {user_words}")
    
    keywords = test_data[0]['keywords']
    print(f"Training keywords: {keywords}")
    
    # Manual keyword matching debug
    keyword_matches = 0
    for keyword in keywords:
        keyword_clean = keyword.lower().strip()
        in_words = keyword_clean in user_words
        in_query = keyword_clean in cleaned_query
        print(f"  Keyword '{keyword_clean}': in_words={in_words}, in_query={in_query}")
        if in_words or in_query:
            keyword_matches += 1
    
    keyword_score = keyword_matches / len(keywords) if keywords else 0
    print(f"Keyword score: {keyword_score}")
    
    # Test full matching
    match_info = matcher.get_match_info(test_input)
    if match_info:
        print(f"Final score: {match_info['score']:.3f}")
        print(f"Threshold: {matcher.min_similarity_threshold}")
        print(f"Match: {'YES' if match_info['score'] >= matcher.min_similarity_threshold else 'NO'}")
    else:
        print("No match found")