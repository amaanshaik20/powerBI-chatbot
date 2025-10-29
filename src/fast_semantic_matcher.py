"""
Fast Semantic Query Matching System
Optimized for speed while maintaining intelligent understanding
"""

import re
from difflib import SequenceMatcher
from typing import List, Dict, Tuple, Optional, Set

class FastSemanticMatcher:
    def __init__(self, training_data: List[Dict]):
        """Initialize the fast semantic matcher"""
        self.training_data = training_data
        self.min_similarity_threshold = 0.25
        
        # Pre-process training data for speed
        self._preprocess_training_data()
        
    def _preprocess_training_data(self):
        """Pre-process training data for faster matching"""
        self.processed_entries = []
        
        for entry in self.training_data:
            processed = {
                'original': entry,
                'question_clean': self.clean_text(entry['question']),
                'question_words': set(self.clean_text(entry['question']).split()),
                'keyword_words': set(),
                'all_words': set()
            }
            
            # Process keywords
            for keyword in entry['keywords']:
                keyword_clean = self.clean_text(keyword)
                processed['keyword_words'].update(keyword_clean.split())
            
            # Combine all words for fast lookup
            processed['all_words'] = processed['question_words'].union(processed['keyword_words'])
            
            self.processed_entries.append(processed)
    
    def clean_text(self, text: str) -> str:
        """Fast text cleaning"""
        return re.sub(r'[^\w\s]', ' ', text.lower().strip())
    
    def fast_similarity(self, text1: str, text2: str) -> float:
        """Fast similarity calculation using word overlap"""
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def classify_intent_fast(self, query_words: List[str]) -> str:
        """Fast intent classification"""
        first_words = query_words[:3] if len(query_words) >= 3 else query_words
        
        # Quick greeting check
        if any(word in ['hi', 'hello', 'hey', 'good', 'morning'] for word in first_words):
            return 'greeting'
        
        # Quick problem check
        if any(word in query_words for word in ['error', 'issue', 'problem', 'not', 'can\'t', 'unable']):
            return 'troubleshooting'
        
        # Quick how-to check
        if 'how' in first_words:
            return 'how_to'
        
        # Quick info check
        if any(word in first_words for word in ['what', 'which', 'explain']):
            return 'information'
        
        return 'general'
    
    def detect_specific_technologies(self, query_words: List[str]) -> Set[str]:
        """Detect specific technologies mentioned in the query"""
        technologies = set()
        query_text = ' '.join(query_words)
        
        # Check for specific technology mentions
        if 'hive' in query_words:
            technologies.add('hive')
        if 'azure' in query_words and 'databricks' in query_words:
            technologies.add('azure_databricks')
        elif 'databricks' in query_words and 'azure' not in query_words:
            technologies.add('databricks')
        if 'sql' in query_words and 'databricks' in query_words:
            technologies.add('databricks_sql')
            
        return technologies
    
    def calculate_technology_match_penalty(self, query_technologies: Set[str], entry_keywords: Set[str]) -> float:
        """Calculate penalty for technology mismatches"""
        penalty = 0.0
        
        # If query mentions specific technology, penalize entries about different technologies
        if 'hive' in query_technologies:
            if 'azure' in entry_keywords and 'databricks' in entry_keywords:
                penalty = 0.5  # Strong penalty for Hive->Databricks mismatch
            elif 'databricks' in entry_keywords and 'azure' not in entry_keywords:
                penalty = 0.3  # Medium penalty for Hive->generic Databricks
        
        elif 'azure_databricks' in query_technologies:
            if 'hive' in entry_keywords and 'cloudera' in entry_keywords:
                penalty = 0.5  # Strong penalty for Databricks->Hive mismatch
                
        return penalty

    def find_best_match(self, user_query: str) -> Optional[Dict]:
        """Fast matching with semantic understanding and technology specificity"""
        query_clean = self.clean_text(user_query)
        query_words = query_clean.split()
        query_word_set = set(query_words)
        
        if not query_words:
            return None
        
        # Get query intent quickly
        query_intent = self.classify_intent_fast(query_words)
        
        # Detect specific technologies in query
        query_technologies = self.detect_specific_technologies(query_words)
        
        best_match = None
        best_score = 0.0
        
        for processed in self.processed_entries:
            # Fast word overlap check first (eliminates most non-matches quickly)
            word_overlap = len(query_word_set.intersection(processed['all_words']))
            if word_overlap == 0:
                continue  # Skip if no word overlap
            
            # Calculate similarities only for potential matches
            question_similarity = self.fast_similarity(query_clean, processed['question_clean'])
            
            # Fast keyword scoring
            keyword_overlap = len(query_word_set.intersection(processed['keyword_words']))
            keyword_score = keyword_overlap / max(len(query_word_set), len(processed['keyword_words'])) if processed['keyword_words'] else 0
            
            # Intent bonus (fast)
            entry_intent = self.classify_intent_fast(list(processed['question_words']))
            intent_bonus = 0.2 if query_intent == entry_intent else 0
            
            # Special greeting handling
            if query_intent == 'greeting' and entry_intent == 'greeting':
                intent_bonus = 0.4
                
                # Special handling for "hi" variations
                if any(variation in user_query.lower() for variation in ['hi', 'hii', 'hiii']):
                    if 'hi' in processed['keyword_words'] or 'hello' in processed['keyword_words']:
                        intent_bonus = 0.6
            
            # Technology-specific matching
            technology_penalty = self.calculate_technology_match_penalty(query_technologies, processed['keyword_words'])
            
            # Combined score with technology penalty
            combined_score = (question_similarity * 0.4) + (keyword_score * 0.4) + intent_bonus - technology_penalty
            
            if combined_score > best_score:
                best_score = combined_score
                best_match = {
                    'entry': processed['original'],
                    'score': combined_score,
                    'question_similarity': question_similarity,
                    'keyword_score': keyword_score,
                    'intent': query_intent,
                    'technology_penalty': technology_penalty
                }
        
        # Return match if it meets threshold
        if best_match and best_match['score'] >= self.min_similarity_threshold:
            return best_match
        
        return None
    
    def get_response(self, user_query: str) -> Tuple[str, bool]:
        """Get response quickly"""
        match = self.find_best_match(user_query)
        
        if match:
            return match['entry']['answer'], True
        else:
            return self.get_fallback_response(), False
    
    def get_fallback_response(self) -> str:
        """Return fast fallback response"""
        return ("I don't have specific information on that topic. "
                "Could you rephrase your question or contact support for assistance?")
    
    def get_match_info(self, user_query: str) -> Optional[Dict]:
        """Get match info for debugging"""
        return self.find_best_match(user_query)


# Simple fallback to original system if needed
class QueryMatcher:
    def __init__(self, training_data: List[Dict]):
        """Fallback to fast semantic matcher"""
        self.matcher = FastSemanticMatcher(training_data)
        
    def get_response(self, user_query: str) -> Tuple[str, bool]:
        return self.matcher.get_response(user_query)
        
    def get_match_info(self, user_query: str) -> Optional[Dict]:
        return self.matcher.get_match_info(user_query)