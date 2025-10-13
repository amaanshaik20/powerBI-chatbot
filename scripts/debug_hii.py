"""
Debug the hii matching issue
"""

import sys
import os
import json

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from query_matcher import QueryMatcher

def debug_hii_matching():
    """Debug hii matching specifically"""
    
    # Load training data
    data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'training_data.json')
    with open(data_file, 'r', encoding='utf-8') as f:
        training_data = json.load(f)
    
    matcher = QueryMatcher(training_data)
    
    # Find hello entry
    hello_entry = None
    for entry in training_data:
        if entry['question'] == 'hello':
            hello_entry = entry
            break
    
    if not hello_entry:
        print("Hello entry not found!")
        return
    
    test_queries = ["hi", "hii", "hiii", "hello"]
    
    print("HII MATCHING DEBUG")
    print("=" * 50)
    print(f"Hello entry keywords: {hello_entry['keywords']}")
    print(f"Threshold: {matcher.min_similarity_threshold}")
    print()
    
    for query in test_queries:
        print(f"Query: '{query}'")
        
        # Test keyword matching
        keyword_score = matcher.keyword_match_score(query, hello_entry['keywords'])
        print(f"  Keyword score: {keyword_score}")
        
        # Test question similarity
        q_sim = matcher.calculate_similarity(
            matcher.clean_text(query),
            matcher.clean_text(hello_entry['question'])
        )
        print(f"  Question similarity: {q_sim}")
        
        # Combined score
        combined = (q_sim * 0.7) + (keyword_score * 0.3)
        
        # Check for greeting boost
        user_lower = query.lower().strip()
        boost = 0
        if any(greeting in user_lower for greeting in ['hi', 'hello', 'hey', 'hii', 'hiii']):
            boost = 0.2
            combined += boost
        
        print(f"  Combined score: {combined} (boost: {boost})")
        
        # Check relevance
        match_info = matcher.find_best_match(query)
        if match_info:
            print(f"  ✅ MATCHES: {match_info['entry']['question']} ({match_info['score']:.3f})")
        else:
            print(f"  ❌ NO MATCH")
        
        print()

if __name__ == "__main__":
    debug_hii_matching()