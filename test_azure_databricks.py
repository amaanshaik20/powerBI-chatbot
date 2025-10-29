#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import EnhancedChatbot

def test_azure_databricks():
    print("Testing Azure Databricks query with corrected training data...")
    chatbot = EnhancedChatbot()
    
    # Test the specific query from user
    query = "How can I connect Power BI Server to Azure Databricks?"
    
    print(f"\nQuery: '{query}'")
    print("-" * 70)
    
    # Get response
    response, is_trained = chatbot.get_response(query)
    
    print(f"Response: {response}")
    print(f"From Training Data: {is_trained}")
    
    # Get detailed match info
    match_info = chatbot.matcher.get_match_info(query)
    
    if match_info:
        print(f"\n🔍 Match Details:")
        print(f"Match Score: {match_info['score']:.3f}")
        print(f"Matched Question: '{match_info['entry']['question']}'")
        
        # Check if it contains the expected elements
        expected_elements = ["Azure Databricks", "Colo-1", "Power Platform", "gateway", "SharePoint"]
        contains_expected = [elem for elem in expected_elements if elem in response]
        
        print(f"\n✅ Expected Elements Found: {contains_expected}")
        
        if "Cloudera" in response:
            print("❌ ERROR: Still returning Hive/Cloudera answer instead of Azure Databricks!")
        else:
            print("✅ SUCCESS: Correct Azure Databricks answer returned!")
    else:
        print("❌ No match found")

    # Also test related variations
    print("\n" + "="*70)
    print("Testing query variations:")
    
    variations = [
        "Power BI Server to Azure Databricks connection",
        "Connect Azure Databricks with Power BI Server",
        "How to connect Power BI to Azure Databricks?"
    ]
    
    for variation in variations:
        print(f"\nVariation: {variation}")
        response, is_trained = chatbot.get_response(variation)
        print(f"Response: {response[:80]}{'...' if len(response) > 80 else ''}")
        print(f"Contains 'Colo-1': {'Colo-1' in response}")

if __name__ == "__main__":
    test_azure_databricks()