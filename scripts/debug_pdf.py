"""
Debug PDF content extraction - show raw text to understand structure
"""

import PyPDF2
import os

def extract_and_show_pdf_content():
    """Extract and display PDF content for debugging"""
    pdf_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Amaan Q&A.pdf')
    
    if not os.path.exists(pdf_path):
        print(f"PDF file not found at: {pdf_path}")
        return
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            print(f"PDF has {len(pdf_reader.pages)} pages")
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                
                print(f"\n{'='*50}")
                print(f"PAGE {page_num + 1}")
                print('='*50)
                print(page_text)
                
                if page_num >= 2:  # Limit to first 3 pages for debugging
                    break
                    
    except Exception as e:
        print(f"Error reading PDF: {e}")

if __name__ == "__main__":
    extract_and_show_pdf_content()