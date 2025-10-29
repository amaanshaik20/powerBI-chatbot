#!/usr/bin/env python3

import PyPDF2
import json

def extract_pdf_text():
    """Extract all text from the PDF to see the format"""
    try:
        with open('data/Amaan Q&A.pdf', 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            full_text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    print(f"\n--- PAGE {page_num + 1} ---")
                    print(page_text[:500] + "..." if len(page_text) > 500 else page_text)
                    full_text += page_text + "\n"
            
            # Save full text for analysis
            with open('pdf_content.txt', 'w', encoding='utf-8') as f:
                f.write(full_text)
            
            print(f"\nFull PDF content saved to pdf_content.txt")
            print(f"Total characters: {len(full_text)}")
            
            return full_text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

if __name__ == "__main__":
    print("Extracting text from Amaan Q&A.pdf...")
    extract_pdf_text()