"""
Enhanced Query Matching System with Semantic Understanding
Implements intelligent matching to understand question context and meaning
"""

import re
import math
from collections import Counter
from difflib import SequenceMatcher
from typing import List, Dict, Tuple, Optional, Set

class SemanticQueryMatcher:
    def __init__(self, training_data: List[Dict]):
        """
        Initialize the semantic query matcher with training data
        
        Args:
            training_data: List of dictionaries containing question, answer, and keywords
        """
        self.training_data = training_data
        self.min_similarity_threshold = 0.25
        
        # Build vocabulary and context understanding
        self.vocabulary = self._build_vocabulary()
        self.question_contexts = self._analyze_question_contexts()
        
    def _build_vocabulary(self) -> Set[str]:
        """Build vocabulary from all training data"""
        vocab = set()
        for entry in self.training_data:
            # Add words from questions
            vocab.update(self.clean_text(entry['question']).split())
            # Add keywords
            for keyword in entry['keywords']:
                vocab.update(self.clean_text(keyword).split())
        return vocab
    
    def _analyze_question_contexts(self) -> Dict[str, List[str]]:
        """Analyze contexts and themes in training questions"""
        contexts = {}
        for i, entry in enumerate(self.training_data):
            question_words = self.clean_text(entry['question']).split()
            keywords = [self.clean_text(kw) for kw in entry['keywords']]
            
            # Identify main topics/themes
            main_topics = []
            for keyword in keywords:
                if len(keyword.split()) <= 2:  # Single words or short phrases
                    main_topics.extend(keyword.split())
            
            contexts[str(i)] = {
                'question_words': question_words,
                'keywords': keywords,
                'main_topics': list(set(main_topics)),
                'entry': entry
            }
        return contexts
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text for better matching"""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def get_semantic_similarity(self, query_words: List[str], target_words: List[str]) -> float:
        """Calculate semantic similarity using word overlap and context"""
        if not query_words or not target_words:
            return 0.0
        
        # Convert to sets for intersection
        query_set = set(query_words)
        target_set = set(target_words)
        
        # Direct word overlap
        common_words = query_set.intersection(target_set)
        overlap_score = len(common_words) / max(len(query_set), len(target_set))
        
        # Contextual similarity (synonyms, related terms)
        contextual_score = self._calculate_contextual_similarity(query_set, target_set)
        
        # Combine scores
        return (overlap_score * 0.6) + (contextual_score * 0.4)
    
    def _calculate_contextual_similarity(self, query_set: Set[str], target_set: Set[str]) -> float:
        """Calculate contextual similarity between word sets"""
        # Define contextual relationships
        power_bi_terms = {'power', 'bi', 'powerbi', 'dashboard', 'report', 'visualization', 'data'}
        database_terms = {'sql', 'database', 'query', 'connection', 'server', 'databricks', 'hive'}
        error_terms = {'error', 'issue', 'problem', 'trouble', 'fail', 'can\'t', 'unable', 'not working'}
        access_terms = {'access', 'permission', 'share', 'view', 'workspace', 'user', 'build'}
        greeting_terms = {'hi', 'hello', 'hey', 'greetings', 'good', 'morning'}
        
        contexts = [power_bi_terms, database_terms, error_terms, access_terms, greeting_terms]
        
        contextual_matches = 0
        total_contexts = len(contexts)
        
        for context in contexts:
            query_in_context = bool(query_set.intersection(context))
            target_in_context = bool(target_set.intersection(context))
            
            if query_in_context and target_in_context:
                contextual_matches += 1
        
        return contextual_matches / total_contexts if total_contexts > 0 else 0.0
    
    def analyze_question_intent(self, query: str) -> Dict[str, any]:
        """Analyze the intent and components of a question"""
        cleaned_query = self.clean_text(query)
        words = cleaned_query.split()
        
        # Identify question type
        question_words = ['what', 'how', 'why', 'where', 'when', 'who', 'which', 'can', 'is', 'are', 'do', 'does']
        has_question_word = any(word in words[:3] for word in question_words)  # Check first 3 words
        
        # Identify key entities and topics
        entities = self._extract_entities(words)
        
        # Determine primary intent
        intent = self._classify_intent(words, entities)
        
        return {
            'is_question': has_question_word or '?' in query,
            'entities': entities,
            'intent': intent,
            'words': words,
            'word_count': len(words)
        }
    
    def _extract_entities(self, words: List[str]) -> Dict[str, List[str]]:
        """Extract key entities from query words"""
        entities = {
            'technologies': [],
            'actions': [],
            'problems': [],
            'objects': []
        }
        
        # Technology entities
        tech_keywords = ['power', 'bi', 'powerbi', 'sql', 'databricks', 'hive', 'azure', 'python']
        entities['technologies'] = [word for word in words if word in tech_keywords]
        
        # Action words
        action_keywords = ['connect', 'export', 'refresh', 'create', 'build', 'share', 'view', 'access']
        entities['actions'] = [word for word in words if word in action_keywords]
        
        # Problem indicators
        problem_keywords = ['error', 'issue', 'problem', 'fail', 'not', 'can\'t', 'unable', 'trouble']
        entities['problems'] = [word for word in words if word in problem_keywords]
        
        # Object entities
        object_keywords = ['dashboard', 'report', 'chart', 'data', 'model', 'workspace', 'server']
        entities['objects'] = [word for word in words if word in object_keywords]
        
        return entities
    
    def _classify_intent(self, words: List[str], entities: Dict[str, List[str]]) -> str:
        """Classify the intent of the query"""
        # Greeting detection
        if any(word in ['hi', 'hello', 'hey', 'good', 'morning'] for word in words[:2]):
            return 'greeting'
        
        # Problem/troubleshooting
        if entities['problems'] or any(word in words for word in ['fix', 'solve', 'resolve']):
            return 'troubleshooting'
        
        # How-to questions
        if 'how' in words[:3] and any(word in entities['actions'] for word in words):
            return 'how_to'
        
        # Information seeking
        if any(word in words[:3] for word in ['what', 'which', 'explain']):
            return 'information'
        
        # Connection/setup
        if any(word in words for word in ['connect', 'setup', 'configure']):
            return 'setup'
        
        # Access/permission issues
        if any(word in words for word in ['access', 'permission', 'share', 'view']):
            return 'access'
        
        return 'general'
    
    def calculate_intent_similarity(self, query_intent: Dict, entry_intent: Dict) -> float:
        """Calculate similarity based on intent analysis"""
        score = 0.0
        
        # Intent type match
        if query_intent['intent'] == entry_intent['intent']:
            score += 0.3
        
        # Entity overlap
        for entity_type in ['technologies', 'actions', 'objects']:
            if query_intent['entities'][entity_type] and entry_intent['entities'][entity_type]:
                common = set(query_intent['entities'][entity_type]).intersection(
                    set(entry_intent['entities'][entity_type])
                )
                if common:
                    score += 0.2
        
        return min(score, 1.0)  # Cap at 1.0
    
    def find_best_match(self, user_query: str) -> Optional[Dict]:
        """Find the best matching response using semantic understanding"""
        cleaned_query = self.clean_text(user_query)
        query_words = cleaned_query.split()
        
        if not query_words:
            return None
        
        # Analyze query intent
        query_intent = self.analyze_question_intent(user_query)
        
        best_match = None
        best_score = 0.0
        
        for entry in self.training_data:
            # Traditional similarity scores
            question_similarity = SequenceMatcher(
                None, cleaned_query, self.clean_text(entry['question'])
            ).ratio()
            
            # Keyword matching
            keyword_words = []
            for keyword in entry['keywords']:
                keyword_words.extend(self.clean_text(keyword).split())
            
            keyword_similarity = self.get_semantic_similarity(query_words, keyword_words)
            
            # Question-to-question semantic similarity
            entry_question_words = self.clean_text(entry['question']).split()
            semantic_similarity = self.get_semantic_similarity(query_words, entry_question_words)
            
            # Intent-based similarity
            entry_intent = self.analyze_question_intent(entry['question'])
            intent_similarity = self.calculate_intent_similarity(query_intent, entry_intent)
            
            # Combined scoring with weights
            combined_score = (
                question_similarity * 0.25 +      # Direct text similarity
                keyword_similarity * 0.25 +       # Keyword matching
                semantic_similarity * 0.30 +      # Semantic word similarity
                intent_similarity * 0.20          # Intent understanding
            )
            
            # Special handling for greetings
            if query_intent['intent'] == 'greeting' and entry_intent['intent'] == 'greeting':
                combined_score += 0.3  # Strong boost for greeting matches
            
            if combined_score > best_score:
                best_score = combined_score
                best_match = {
                    'entry': entry,
                    'score': combined_score,
                    'question_similarity': question_similarity,
                    'keyword_similarity': keyword_similarity,
                    'semantic_similarity': semantic_similarity,
                    'intent_similarity': intent_similarity,
                    'query_intent': query_intent,
                    'entry_intent': entry_intent
                }
        
        # Return match if it meets threshold
        if best_match and best_match['score'] >= self.min_similarity_threshold:
            return best_match
        
        return None
    
    def get_response(self, user_query: str) -> Tuple[str, bool]:
        """Get response for user query using semantic understanding"""
        match = self.find_best_match(user_query)
        
        if match:
            return match['entry']['answer'], True
        else:
            return self.get_fallback_response(), False
    
    def get_fallback_response(self) -> str:
        """Return intelligent fallback response"""
        return ("I understand you're asking about something, but I don't have specific information on that topic. "
                "Could you please rephrase your question or contact the support team for more detailed assistance?")
    
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
            "question": "How can I connect Hive server to Power BI?",
            "answer": "Use Cloudera drivers (not paid ones). Ensure TLS 1.2 or higher and a 64-bit System DSN.",
            "keywords": ["hive", "server", "power", "bi", "connect", "cloudera", "drivers"]
        }
    ]
    
    matcher = SemanticQueryMatcher(sample_data)
    
    # Test queries with variations
    test_queries = [
        "hi there",
        "How do I connect Power BI to Hive?",
        "Power BI Hive connection setup",
        "connecting hive with powerbi",
        "what's the weather like"
    ]
    
    print("Semantic Query Matching Test Results:")
    print("=" * 50)
    
    for query in test_queries:
        response, is_trained = matcher.get_response(query)
        match_info = matcher.get_match_info(query)
        
        print(f"\nQuery: '{query}'")
        print(f"Response: {response}")
        print(f"From training data: {is_trained}")
        
        if match_info:
            print(f"Overall Score: {match_info['score']:.3f}")
            print(f"  - Question Similarity: {match_info['question_similarity']:.3f}")
            print(f"  - Keyword Similarity: {match_info['keyword_similarity']:.3f}")
            print(f"  - Semantic Similarity: {match_info['semantic_similarity']:.3f}")
            print(f"  - Intent Similarity: {match_info['intent_similarity']:.3f}")
            print(f"  - Query Intent: {match_info['query_intent']['intent']}")
        else:
            print("No match found")