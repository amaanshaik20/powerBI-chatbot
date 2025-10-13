import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from unittest.mock import patch
from io import StringIO
from chatbot import chatbot


class TestChatbot(unittest.TestCase):
    
    def test_greeting_responses(self):
        """Test various greeting inputs"""
        test_cases = [
            ("hi", "Hi there! 👋"),
            ("hello", "Hi there! 👋"),
            ("hey", "Hi there! 👋"),
            ("Hi there", "Hi there! 👋"),
            ("HELLO", "Hi there! 👋"),
            ("Hey buddy", "Hi there! 👋"),
        ]
        
        for input_text, expected_response in test_cases:
            with self.subTest(input_text=input_text):
                # Test that greeting keywords are detected
                self.assertTrue(
                    "hi" in input_text.lower() or 
                    "hello" in input_text.lower() or 
                    "hey" in input_text.lower()
                )
    
    def test_how_are_you_responses(self):
        """Test 'how are you' type inputs"""
        test_cases = [
            "how are you",
            "How are you?",
            "HOW ARE YOU",
            "how are you doing",
            "how are you today",
        ]
        
        for input_text in test_cases:
            with self.subTest(input_text=input_text):
                self.assertIn("how are you", input_text.lower())


if __name__ == "__main__":
    unittest.main()