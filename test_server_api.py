#!/usr/bin/env python3

import requests
import json

def test_server():
    print("Testing web server API...")
    
    # Test the chat endpoint
    url = "http://localhost:8001/chat"
    
    test_queries = [
        "Hello",
        "Why is there a discrepancy between the number shown on screen and the exported data from Power BI?",
        "How can I connect Hive server to Power BI?"
    ]
    
    for query in test_queries:
        try:
            response = requests.post(url, 
                json={'message': query}, 
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Query: {query[:50]}{'...' if len(query) > 50 else ''}")
                print(f"   Response: {data.get('response', 'No response')[:80]}...")
                print(f"   Status: {data.get('status', 'unknown')}")
            else:
                print(f"❌ Query failed with status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error: {e}")
            break
        
        print("-" * 60)

if __name__ == "__main__":
    test_server()