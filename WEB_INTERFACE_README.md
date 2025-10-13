# Chatbot Web Interface

## Features
- Modern, responsive chat interface
- Real-time messaging with your trained chatbot
- Statistics display showing conversation count and training data
- Mobile-friendly design
- Typing indicators for better user experience

## How to Run

1. Make sure all dependencies are installed:
   ```
   pip install flask flask-cors pypdf2
   ```

2. Start the web server:
   ```
   python app.py
   ```

3. Open your browser and go to:
   ```
   http://localhost:5000
   ```

## Features of the Interface

- **Chat Bubbles**: Messages appear in styled bubbles with different colors for user and bot
- **Typing Indicator**: Shows when the bot is processing your message
- **Statistics**: Real-time display of conversation count and training data size
- **Responsive Design**: Works on desktop and mobile devices
- **Gradient Theme**: Modern purple gradient design

## Testing Your Chatbot

You can test all the features you've built:
- Greetings: Try "hi", "hello", "hii"
- Power BI Questions: Ask "what is power bi" or other Power BI related questions
- Programming Questions: Ask about Python, programming concepts
- Unknown Topics: Try random questions to see fallback responses

The interface connects to your existing EnhancedChatbot with all the training data from the PDF extraction and query matching improvements you've implemented.