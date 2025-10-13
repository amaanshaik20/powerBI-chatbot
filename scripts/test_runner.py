# Manual Testing Script for Chatbot
# Run this to automatically test various inputs with your chatbot

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))

from test_data import all_test_data

def run_manual_tests():
    """
    This script helps you manually test your chatbot with predefined inputs.
    Copy and paste these inputs into your running chatbot to test responses.
    """
    
    print("CHATBOT MANUAL TEST SCRIPT")
    print("=" * 50)
    print("Copy and paste these inputs into your chatbot to test:")
    print()
    
    for category, inputs in all_test_data.items():
        if category == "edge_cases":  # Skip exit commands for manual testing
            continue
            
        print(f"{category.upper()} TESTS:")
        print("-" * 30)
        
        for i, test_input in enumerate(inputs[:5], 1):  # Show first 5 of each category
            print(f"Test {i}: {test_input}")
        
        if len(inputs) > 5:
            print(f"... and {len(inputs) - 5} more")
        print()
    
    print("TESTING TIPS:")
    print("- Test one input at a time")
    print("- Check if responses match expected behavior")
    print("- Try variations of each input")
    print("- Test with different capitalization")
    print("- Don't forget to test 'exit' to end the session")

if __name__ == "__main__":
    run_manual_tests()