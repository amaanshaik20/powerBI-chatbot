#!/usr/bin/env python3

import json

# Load from JSON and recreate the Python file
with open('data/training_data.json', 'r', encoding='utf-8') as f:
    training_data = json.load(f)

# Update the Azure Databricks entry keywords to make them more specific
for entry in training_data:
    if "Azure Databricks" in entry['question'] and "Colo-1" in entry['answer']:
        if "azure_databricks" not in entry['keywords']:
            entry['keywords'].append("azure_databricks")
        print(f"Updated Azure Databricks entry keywords: {entry['keywords']}")

# Recreate the Python file
python_content = '''# Training Data for Chatbot
# Format: {"question": "user query", "answer": "chatbot response", "keywords": ["key", "words"]}

import json

training_data = [
'''

for entry in training_data:
    python_content += f'''    {{
        "question": "{entry['question']}",
        "answer": "{entry['answer']}",
        "keywords": {entry['keywords']}
    }},
'''

python_content += ''']

def save_training_data():
    """Save training data to JSON file"""
    with open('data/training_data.json', 'w', encoding='utf-8') as f:
        json.dump(training_data, f, indent=2, ensure_ascii=False)
    print(f"Training data saved! Total entries: {len(training_data)}")

def load_training_data():
    """Load training data from JSON file"""
    try:
        with open('data/training_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Training data file not found. Creating new one...")
        save_training_data()
        return training_data

if __name__ == "__main__":
    save_training_data()
    print("\\nSample training entries:")
    for i, entry in enumerate(training_data[:3], 1):
        print(f"{i}. Q: {entry['question']}")
        print(f"   A: {entry['answer']}")
        print(f"   Keywords: {entry['keywords']}\\n")'''

# Write the new file
with open('data/training_data_fixed.py', 'w', encoding='utf-8') as f:
    f.write(python_content)

print("Fixed training data file created!")
print(f"Total entries: {len(training_data)}")

# Save updated JSON
with open('data/training_data.json', 'w', encoding='utf-8') as f:
    json.dump(training_data, f, indent=2, ensure_ascii=False)

print("Updated JSON file saved!")