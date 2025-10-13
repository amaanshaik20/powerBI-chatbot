"""
Query Matching System for Chatbot
Implements similarity matching to find best responses from training data
"""

import re
from difflib import SequenceMatcher
from typing import List, Dict, Tuple, Optional

class QueryMatcher:
    def __init__(self, training_data: List[Dict]):
        """
        Initialize the query matcher with training data
        
        Args:
            training_data: List of dictionaries containing question, answer, and keywords
        """
        self.training_data = training_data
        self.min_similarity_threshold = 0.25  # Balanced threshold for good matching vs fallback
        
    def clean_text(self, text: str) -> str:
        """Clean and normalize text for better matching"""
        # Convert to lowercase
        text = text.lower().strip()
        
        # Remove punctuation and extra spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts using SequenceMatcher"""
        return SequenceMatcher(None, text1, text2).ratio()
    
    def keyword_match_score(self, user_query: str, keywords: List[str]) -> float:
        """Calculate how many keywords from training data appear in user query"""
        user_words = set(self.clean_text(user_query).split())
        cleaned_query = self.clean_text(user_query)
        
        # Check for exact word matches (not substrings)
        keyword_matches = 0
        for keyword in keywords:
            keyword_clean = keyword.lower().strip()
            
            # Special handling for greetings - be more flexible
            if keyword_clean in ['hi', 'hello', 'hey']:
                # Check for variations like 'hii', 'hiii', 'heyyy'
                if keyword_clean == 'hi' and any(variation in cleaned_query for variation in ['hi', 'hii', 'hiii']):
                    keyword_matches += 1
                elif keyword_clean == 'hello' and any(variation in cleaned_query for variation in ['hello', 'helo', 'hllo']):
                    keyword_matches += 1
                elif keyword_clean == 'hey' and any(variation in cleaned_query for variation in ['hey', 'heey', 'heyy']):
                    keyword_matches += 1
                elif keyword_clean in user_words:
                    keyword_matches += 1
            else:
                # Use EXACT word matching only - no substring matching
                # This prevents "ai" from matching "bi" in "power bi"
                if keyword_clean in user_words:
                    keyword_matches += 1
                # Only allow substring matching for compound words (3+ characters)
                elif len(keyword_clean) >= 3 and keyword_clean in cleaned_query:
                    # Additional check: ensure it's not a false partial match
                    # For example, "ai" should not match in "power bi"
                    import re
                    # Use word boundaries to ensure exact matches
                    if re.search(r'\b' + re.escape(keyword_clean) + r'\b', cleaned_query):
                        keyword_matches += 1
        
        if not keywords:
            return 0.0
        
        return keyword_matches / len(keywords)
    
    def is_relevant_match(self, user_query: str, entry: Dict, combined_score: float) -> bool:
        """Check if a match is actually relevant to the user query"""
        
        # If score is very high, it's definitely relevant
        if combined_score > 0.6:
            return True
        
        # Check for topic relevance - look for domain-specific keywords
        user_words = set(self.clean_text(user_query).split())
        
        # Technical domains that should match our training data
        tech_domains = {
            'power_bi': ['power', 'bi', 'powerbi', 'dashboard', 'report', 'refresh', 'dataflow', 'gateway', 'databricks', 'azure', 'jira'],
            'programming': ['python', 'programming', 'code', 'language', 'ai', 'artificial', 'intelligence'],
            'general': ['hello', 'hi', 'hey', 'greetings', 'thank', 'thanks', 'goodbye', 'bye', 'morning']
        }
        
        # Check if user query contains words from our known domains
        query_has_known_domain = False
        for domain_words in tech_domains.values():
            if any(word in user_words for word in domain_words):
                query_has_known_domain = True
                break
        
        # Check if the matched entry is from our known domains
        entry_keywords = [kw.lower() for kw in entry['keywords']]
        entry_has_known_domain = False
        for domain_words in tech_domains.values():
            if any(word in entry_keywords for word in domain_words):
                entry_has_known_domain = True
                break
        
        # Special case for greetings - be more lenient
        if any(greeting in entry['keywords'] for greeting in ['hello', 'hi', 'hey', 'greetings']):
            user_lower = user_query.lower().strip()
            if any(greeting in user_lower for greeting in ['hi', 'hello', 'hey', 'hii', 'hiii']):
                return True  # Always allow greeting matches
        
        # If both query and entry are in known domains, and score is reasonable, it's relevant
        if query_has_known_domain and entry_has_known_domain and combined_score > 0.28:
            return True
        
        # If query is completely unrelated (no known domain words), reject weak matches
        if not query_has_known_domain and combined_score < 0.5:
            return False
        
        # Default to accepting the match if score is above threshold
        return True

    def find_best_match(self, user_query: str) -> Optional[Dict]:
        """
        Find the best matching response from training data
        
        Args:
            user_query: The user's input query
            
        Returns:
            Dictionary with best match info or None if no good match found
        """
        cleaned_query = self.clean_text(user_query)
        
        if not cleaned_query:
            return None
        
        best_match = None
        best_score = 0.0
        
        for entry in self.training_data:
            # Calculate similarity with question
            question_similarity = self.calculate_similarity(
                cleaned_query, 
                self.clean_text(entry['question'])
            )
            
            # Calculate keyword match score
            keyword_score = self.keyword_match_score(user_query, entry['keywords'])
            
            # Prioritize question similarity over keyword matching for better answers
            combined_score = (question_similarity * 0.7) + (keyword_score * 0.3)
            
            # Check if this is a greeting interaction
            is_greeting_entry = any(greeting in entry['keywords'] for greeting in ['hello', 'hi', 'hey', 'greetings'])
            is_greeting_query = False
            
            if is_greeting_entry:
                user_lower = user_query.lower().strip()
                # More comprehensive greeting detection including variations
                greeting_patterns = ['hi', 'hii', 'hiii', 'hiiii', 'hello', 'helo', 'hllo', 'hey', 'heey', 'heyy']
                if any(pattern == user_lower or pattern in user_lower for pattern in greeting_patterns):
                    is_greeting_query = True
                    combined_score += 0.3  # Strong boost for greeting matches
            
            # Apply relevance penalty ONLY for non-greeting weak matches
            if (not is_greeting_query and not is_greeting_entry and 
                keyword_score < 0.3 and question_similarity < 0.3):
                combined_score *= 0.7  # Reduce score for weak matches
            
            if combined_score > best_score:
                best_score = combined_score
                best_match = {
                    'entry': entry,
                    'score': combined_score,
                    'question_similarity': question_similarity,
                    'keyword_score': keyword_score
                }
        
        # Return match only if it meets minimum threshold AND is relevant
        if (best_match and 
            best_match['score'] >= self.min_similarity_threshold and
            self.is_relevant_match(user_query, best_match['entry'], best_match['score'])):
            return best_match
        
        return None
    
    def get_response(self, user_query: str) -> Tuple[str, bool]:
        """
        Get response for user query
        
        Args:
            user_query: The user's input
            
        Returns:
            Tuple of (response_text, is_from_training_data)
        """
        match = self.find_best_match(user_query)
        
        if match:
            return match['entry']['answer'], True
        else:
            return self.get_fallback_response(), False
    
    def get_fallback_response(self) -> str:
        """Return fallback response when no match is found"""
        return ("Currently I don't have knowledge on this topic. "
                "Please contact the respective person for more information.")
    
    def add_training_entry(self, question: str, answer: str, keywords: List[str]):
        """Add new training entry"""
        new_entry = {
            'question': question,
            'answer': answer,
            'keywords': keywords
        }
        self.training_data.append(new_entry)
    
    def get_match_info(self, user_query: str) -> Optional[Dict]:
        """Get detailed matching information for debugging"""
        return self.find_best_match(user_query)


# Example usage and testing
if __name__ == "__main__":
    # Sample training data for testing
    sample_data = [
        {
            "question": "hello",
            "answer": "Hello! How can I help you?",
            "keywords": ["hello", "hi", "hey", "greetings"]
        },
        {
            "question": "what is python",
            "answer": "Python is a programming language.",
            "keywords": ["python", "programming", "language"]
        }
    ]
    
    matcher = QueryMatcher(sample_data)
    
    # Test queries
    test_queries = [
        "hi there",
        "tell me about python",
        "what's the weather like",
        "hello world"
    ]
    
    print("Query Matching Test Results:")
    print("=" * 40)
    
    for query in test_queries:
        response, is_trained = matcher.get_response(query)
        match_info = matcher.get_match_info(query)
        
        print(f"\nQuery: '{query}'")
        print(f"Response: {response}")
        print(f"From training data: {is_trained}")
        
        if match_info:
            print(f"Match score: {match_info['score']:.3f}")
        else:
            print("No match found")