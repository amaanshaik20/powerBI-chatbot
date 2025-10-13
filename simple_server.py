#!/usr/bin/env python3
"""
Simple HTTP Server for Chatbot Interface
This creates a basic web server without needing Flask
"""

import http.server
import socketserver
import json
import urllib.parse
import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from chatbot import EnhancedChatbot
    CHATBOT_AVAILABLE = True
    chatbot = EnhancedChatbot()
    print("✓ Chatbot loaded successfully")
except ImportError as e:
    CHATBOT_AVAILABLE = False
    print(f"⚠ Could not load chatbot: {e}")

class ChatbotRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)

    def do_POST(self):
        if self.path == '/chat':
            self.handle_chat_request()
        else:
            self.send_error(404)

    def do_GET(self):
        if self.path == '/':
            self.path = '/simple_interface.html'
        elif self.path == '/stats':
            self.handle_stats_request()
            return
        super().do_GET()

    def handle_chat_request(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            message = data.get('message', '').strip()
            
            if not message:
                self.send_json_response({'error': 'Empty message'}, 400)
                return

            if CHATBOT_AVAILABLE:
                response = chatbot.get_response(message)
            else:
                # Fallback responses if chatbot isn't available
                fallback_responses = {
                    'hi': 'Hello! How can I help you today?',
                    'hello': 'Hi there! What would you like to know?',
                    'what is power bi': 'Microsoft Power BI is a business analytics platform by Microsoft.',
                    'what is python': 'Python is a high-level programming language.',
                }
                response = fallback_responses.get(message.lower(), 
                    "I'm sorry, the chatbot service is not available right now.")

            self.send_json_response({
                'response': response,
                'status': 'success'
            })

        except Exception as e:
            print(f"Error handling chat request: {e}")
            self.send_json_response({
                'error': str(e),
                'status': 'error'
            }, 500)

    def handle_stats_request(self):
        try:
            if CHATBOT_AVAILABLE:
                stats = {
                    'total_questions': len(chatbot.conversation_history),
                    'training_data_count': len(chatbot.training_data),
                    'chatbot_available': True
                }
            else:
                stats = {
                    'total_questions': 0,
                    'training_data_count': 0,
                    'chatbot_available': False
                }
            
            self.send_json_response(stats)
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)

    def send_json_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def start_server(port=8000):
    """Start the simple HTTP server"""
    try:
        with socketserver.TCPServer(("", port), ChatbotRequestHandler) as httpd:
            print(f"🚀 Chatbot server starting...")
            print(f"📱 Open your browser and go to: http://localhost:{port}")
            print(f"🔧 Chatbot status: {'✓ Available' if CHATBOT_AVAILABLE else '⚠ Fallback mode'}")
            print(f"🛑 Press Ctrl+C to stop the server")
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Start chatbot web server')
    parser.add_argument('--port', type=int, default=8000, help='Port to run server on')
    args = parser.parse_args()
    
    start_server(args.port)