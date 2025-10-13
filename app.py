from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
import os

# Add the src directory to the path so we can import our chatbot
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import EnhancedChatbot

app = Flask(__name__)
CORS(app)

# Initialize the chatbot
chatbot = EnhancedChatbot()

@app.route('/')
def home():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from the frontend"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Get response from chatbot
        response = chatbot.get_response(user_message)
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/stats')
def stats():
    """Get chatbot statistics"""
    try:
        stats = {
            'total_questions': len(chatbot.conversation_history),
            'training_data_count': len(chatbot.training_data),
            'last_question': chatbot.conversation_history[-1] if chatbot.conversation_history else None
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Chatbot Web Interface...")
    print("Chat interface will be available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)