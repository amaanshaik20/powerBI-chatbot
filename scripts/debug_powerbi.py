"""
Test Power BI question matching specifically
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

def test_powerbi_question():
    """Test Power BI question matching"""
    
    training_data = load_training_data()
    matcher = QueryMatcher(training_data)
    
    question = "what is powerbi"
    
    print("POWER BI QUESTION MATCHING DEBUG")
    print("=" * 50)
    print(f"Question: '{question}'")
    print()
    
    # Find all potential matches with scores
    cleaned_query = matcher.clean_text(question)
    print(f"Cleaned query: '{cleaned_query}'")
    print()
    
    matches = []
    for i, entry in enumerate(training_data):
        question_similarity = matcher.calculate_similarity(
            cleaned_query, 
            matcher.clean_text(entry['question'])
        )
        
        keyword_score = matcher.keyword_match_score(question, entry['keywords'])
        combined_score = (question_similarity * 0.7) + (keyword_score * 0.3)
        
        if keyword_score > 0 or question_similarity > 0.1:  # Show relevant matches
            matches.append({
                'index': i,
                'question': entry['question'],
                'answer': entry['answer'][:80] + "...",
                'keywords': entry['keywords'],
                'question_sim': question_similarity,
                'keyword_score': keyword_score,
                'combined_score': combined_score
            })
    
    # Sort by combined score
    matches.sort(key=lambda x: x['combined_score'], reverse=True)
    
    print("TOP MATCHES:")
    print("-" * 50)
    for i, match in enumerate(matches[:5]):
        print(f"{i+1}. Score: {match['combined_score']:.3f}")
        print(f"   Q Sim: {match['question_sim']:.3f} | K Score: {match['keyword_score']:.3f}")
        print(f"   Question: {match['question']}")
        print(f"   Answer: {match['answer']}")
        print(f"   Keywords: {match['keywords']}")
        print()
    
    # Show final result
    response, is_trained = matcher.get_response(question)
    print("FINAL RESULT:")
    print("-" * 50)
    print(f"Response: {response}")
    print(f"From training: {is_trained}")

if __name__ == "__main__":
    test_powerbi_question()