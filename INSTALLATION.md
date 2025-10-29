# Power BI Chatbot - Installation & Setup Guide

## Requirements

### Python Version
- Python 3.8 or higher

### Dependencies

#### Essential Dependencies (Minimal Installation)
```bash
pip install -r requirements-minimal.txt
```

#### Full Development Dependencies  
```bash
pip install -r requirements.txt
```

## Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd chatbot1
   ```

2. **Install dependencies**
   ```bash
   # For minimal installation (production)
   pip install -r requirements-minimal.txt
   
   # OR for full development setup
   pip install -r requirements.txt
   ```

3. **Run the chatbot**
   
   **Web Interface (Recommended):**
   ```bash
   python simple_server.py
   ```
   Then open your browser to: http://localhost:8000
   
   **Command Line Interface:**
   ```bash
   python src/chatbot.py
   ```

## Project Structure

```
chatbot1/
├── data/
│   ├── training_data.py    # Training Q&A data
│   └── training_data.json  # JSON version of training data
├── src/
│   ├── chatbot.py                 # Main chatbot class
│   ├── fast_semantic_matcher.py   # Optimized semantic matching
│   └── semantic_matcher.py        # Original semantic matcher
├── simple_server.py           # Web server for chatbot interface
├── simple_interface.html      # Web UI with Wipro branding
├── requirements.txt           # Full dependencies
├── requirements-minimal.txt   # Essential dependencies only
└── tests/                     # Various test scripts
```

## Key Features

- **Fast Semantic Understanding**: Sub-millisecond response times
- **Technology-Specific Matching**: Distinguishes between Hive, Azure Databricks, etc.
- **Web Interface**: Corporate-branded UI with clickable links
- **Extensible Training Data**: Easy to add new Q&A pairs
- **No External AI APIs**: Runs completely offline

## Dependencies Explained

### Essential Dependencies (Required)
- **requests**: Used for HTTP testing and API interactions
- **PyPDF2**: Used in scripts for extracting Q&A from PDF documents

### Built-in Python Modules (No Installation Needed)
- `json`: Data serialization
- `http.server`, `socketserver`: Web server functionality  
- `urllib.parse`: URL processing
- `re`: Regular expressions for text processing
- `difflib`: Text similarity calculations
- `collections`, `typing`: Data structures and type hints
- `os`, `sys`, `pathlib`: File system operations
- `time`, `math`: Utilities

### Development Dependencies (Optional)
- **black**: Code formatting
- **flake8**: Code linting
- **mypy**: Type checking

## Troubleshooting

### Port Already in Use
If you get a "port already in use" error:
```bash
# Start on a different port
python -c "from simple_server import start_server; start_server(8001)"
```

### Import Errors
Make sure you're running commands from the project root directory:
```bash
cd chatbot1
python simple_server.py
```

### Training Data Issues
If training data gets corrupted:
```bash
python data/training_data.py
```

## Adding New Q&A Pairs

1. Edit `data/training_data.py`
2. Add your new entry to the `training_data` list
3. Run: `python data/training_data.py` to regenerate JSON
4. Restart the server

Example:
```python
{
    "question": "Your new question?",
    "answer": "Your detailed answer here.",
    "keywords": ["relevant", "keywords", "for", "matching"]
}
```