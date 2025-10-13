"""
Enhanced Chatbot with Training Data and Query Matching
Uses machine learning-like matching to find best responses from training data
"""

import os
import sys
import json

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data'))

from query_matcher import QueryMatcher

class EnhancedChatbot:
    def __init__(self):
        """Initialize the enhanced chatbot with training data"""
        self.training_data = self.load_training_data()
        self.matcher = QueryMatcher(self.training_data)
        self.conversation_history = []
        
    def load_training_data(self):
        """Load training data from JSON file"""
        data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'training_data.json')
        
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"✅ Loaded {len(data)} training entries")
                return data
        except FileNotFoundError:
            print("⚠️  Training data not found. Creating basic fallback data...")
            return self.create_fallback_data()
        except json.JSONDecodeError as e:
            print(f"❌ Error loading training data: {e}")
            return self.create_fallback_data()
    
    def create_fallback_data(self):
        """Create basic fallback training data if file is missing"""
        return [
            {
                "question": "hello",
                "answer": "Hello! How can I help you today?",
                "keywords": ["hello", "hi", "hey", "greetings"]
            },
            {
                "question": "how are you",
                "answer": "I'm doing well, thank you for asking!",
                "keywords": ["how", "are", "you", "doing"]
            }
        ]
    
    def get_response(self, user_input):
        """Get chatbot response for user input"""
        # Check for exit command first
        if user_input.lower().strip() in ['exit', 'quit', 'bye', 'goodbye']:
            return "exit"
        
        # Get response from query matcher
        response, is_from_training = self.matcher.get_response(user_input)
        
        # Log the conversation
        self.conversation_history.append({
            'user': user_input,
            'bot': response,
            'from_training': is_from_training
        })
        
        return response
    
    def show_debug_info(self, user_input):
        """Show debug information about the matching process"""
        match_info = self.matcher.get_match_info(user_input)
        
        if match_info:
            print(f"\n🔍 Debug Info:")
            print(f"   Best match: '{match_info['entry']['question']}'")
            print(f"   Overall score: {match_info['score']:.3f}")
            print(f"   Question similarity: {match_info['question_similarity']:.3f}")
            print(f"   Keyword score: {match_info['keyword_score']:.3f}")
        else:
            print(f"\n🔍 Debug Info: No good match found (using fallback)")
    
    def run(self, debug_mode=False):
        """Run the chatbot main loop"""
        print("🤖 Enhanced Chatbot with Training Data")
        print("=" * 45)
        print(f"📚 Loaded {len(self.training_data)} training entries")
        print("💡 I can answer questions based on my training data")
        print("❓ If I don't know something, I'll let you know!")
        print("🚪 Type 'exit' to end the chat")
        
        if debug_mode:
            print("🔍 Debug mode: ON (showing match scores)")
        
        print("\nChatbot: Hello! What would you like to know?")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    print("Chatbot: Please say something!")
                    continue
                
                response = self.get_response(user_input)
                
                if response == "exit":
                    print("Chatbot: Goodbye! Thanks for chatting with me! 👋")
                    break
                
                print(f"Chatbot: {response}")
                
                # Show debug info if enabled
                if debug_mode:
                    self.show_debug_info(user_input)
                    
            except KeyboardInterrupt:
                print("\n\nChatbot: Goodbye! Thanks for chatting! 👋")
                break
            except Exception as e:
                print(f"Chatbot: Sorry, I encountered an error: {e}")
    
    def show_stats(self):
        """Show conversation statistics"""
        if not self.conversation_history:
            print("No conversation history yet.")
            return
        
        total_responses = len(self.conversation_history)
        training_responses = sum(1 for entry in self.conversation_history if entry['from_training'])
        fallback_responses = total_responses - training_responses
        
        print(f"\n📊 Conversation Statistics:")
        print(f"   Total responses: {total_responses}")
        print(f"   From training data: {training_responses} ({training_responses/total_responses*100:.1f}%)")
        print(f"   Fallback responses: {fallback_responses} ({fallback_responses/total_responses*100:.1f}%)")

def main():
    """Main function to run the chatbot"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Enhanced Chatbot with Training Data')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--stats', action='store_true', help='Show stats after conversation')
    
    args = parser.parse_args()
    
    # Initialize and run chatbot
    chatbot = EnhancedChatbot()
    chatbot.run(debug_mode=args.debug)
    
    # Show stats if requested
    if args.stats:
        chatbot.show_stats()

if __name__ == "__main__":
    main()