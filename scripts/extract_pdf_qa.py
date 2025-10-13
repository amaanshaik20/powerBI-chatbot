"""
Extract Q&A content from Amaan Q&A.pdf and convert to training data format
"""

import PyPDF2
import re
import json
import os

def extract_pdf_content(pdf_path):
    """Extract text content from PDF file"""
    text_content = ""
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    text_content += page_text + "\n"
        return text_content
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def parse_qa_content(text):
    """Parse Q&A content from extracted text"""
    qa_pairs = []
    
    # Clean up text and normalize line breaks
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    text = text.replace('Internal - General Use', '')  # Remove header
    
    # Find all Query blocks using regex
    query_pattern = r'Query \d+:([^Q]+?)(?=Query \d+:|$)'
    matches = re.findall(query_pattern, text, re.DOTALL)
    
    for match in matches:
        content = match.strip()
        
        # Split by Q: and A: to find question and answer
        if 'Q:' in content and 'A:' in content:
            # Extract question (everything after Q: until A:)
            q_match = re.search(r'Q:\s*(.+?)A:', content, re.DOTALL)
            # Extract answer (everything after A:)
            a_match = re.search(r'A:\s*(.+)', content, re.DOTALL)
            
            if q_match and a_match:
                question = q_match.group(1).strip()
                answer = a_match.group(1).strip()
                
                # Clean up question and answer
                question = re.sub(r'\s+', ' ', question)
                answer = re.sub(r'\s+', ' ', answer)
                
                # Generate keywords from question
                keywords = generate_keywords(question + " " + answer)
                
                qa_pairs.append({
                    "question": question,
                    "answer": answer,
                    "keywords": keywords
                })
    
    return qa_pairs

def generate_keywords(question):
    """Generate keywords from question text"""
    # Remove common words and extract meaningful terms
    common_words = {'the', 'is', 'in', 'to', 'and', 'a', 'of', 'for', 'on', 'with', 'how', 'what', 'when', 'where', 'why', 'can', 'do', 'does'}
    
    # Extract words and clean them
    words = re.findall(r'\b\w+\b', question.lower())
    keywords = [word for word in words if word not in common_words and len(word) > 2]
    
    # Add some specific Power BI related keywords based on content
    powerbi_keywords = []
    question_lower = question.lower()
    
    if 'power bi' in question_lower:
        powerbi_keywords.extend(['power', 'bi', 'powerbi'])
    if 'refresh' in question_lower:
        powerbi_keywords.append('refresh')
    if 'dataset' in question_lower:
        powerbi_keywords.append('dataset')
    if 'gateway' in question_lower:
        powerbi_keywords.append('gateway')
    if 'dataflow' in question_lower:
        powerbi_keywords.append('dataflow')
    if 'report' in question_lower:
        powerbi_keywords.append('report')
    if 'connection' in question_lower:
        powerbi_keywords.append('connection')
    if 'error' in question_lower:
        powerbi_keywords.extend(['error', 'issue', 'problem'])
    
    # Combine and deduplicate
    all_keywords = list(set(keywords + powerbi_keywords))
    
    return all_keywords[:8]  # Limit to 8 keywords

def main():
    """Main function to extract and process PDF content"""
    pdf_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Amaan Q&A.pdf')
    
    if not os.path.exists(pdf_path):
        print(f"PDF file not found at: {pdf_path}")
        return
    
    print("Extracting content from PDF...")
    text_content = extract_pdf_content(pdf_path)
    
    if not text_content:
        print("Failed to extract content from PDF")
        return
    
    print("Parsing Q&A pairs...")
    qa_pairs = parse_qa_content(text_content)
    
    print(f"Found {len(qa_pairs)} Q&A pairs")
    
    # Display first few Q&A pairs for verification
    print("\nSample Q&A pairs:")
    for i, qa in enumerate(qa_pairs[:3]):
        print(f"\n{i+1}. Question: {qa['question']}")
        print(f"   Answer: {qa['answer'][:100]}...")
        print(f"   Keywords: {qa['keywords']}")
    
    # Save extracted data
    output_file = os.path.join(os.path.dirname(__file__), 'extracted_qa.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(qa_pairs, f, indent=2, ensure_ascii=False)
    
    print(f"\nExtracted Q&A data saved to: {output_file}")
    
    return qa_pairs

if __name__ == "__main__":
    main()