#!/usr/bin/env python3

import json
import re

# Extract all Q&A pairs from the PDF content
pdf_qa_pairs = [
    {
        "question": "Why is there a discrepancy between the number shown on screen and the exported data from Power BI?",
        "answer": "The issue arises when attributes are added to the visualization. Removing them aligns the data. Exported CSV values are static and not bound by model logic, so summing them directly may be unsafe.",
        "keywords": ["power", "bi", "export", "data", "discrepancy", "csv", "visualization", "attributes", "mismatch", "screen"]
    },
    {
        "question": "How can I connect Power BI Server to Azure Databricks?",
        "answer": "Use the \"Azure Databricks\" connector (not \"Databricks\") via the Colo-1 Power Platform gateway. Follow the instructions on the Power BI Gateway SharePoint page.",
        "keywords": ["power", "bi", "server", "azure", "databricks", "connector", "gateway", "connection", "colo-1", "platform", "sharepoint", "azure_databricks"]
    },
    {
        "question": "Why does my Power BI report fail during scheduled refresh but works manually?",
        "answer": "It could be due to dynamic file usage (e.g., daily Excel files). Ensure the file format (e.g., XLSX) and hosting (e.g., SharePoint) are consistent and supported.",
        "keywords": ["power", "bi", "report", "fail", "scheduled", "refresh", "manual", "dynamic", "excel", "xlsx", "sharepoint"]
    },
    {
        "question": "How can I refresh a Power BI report if I don't have access or know the developer?",
        "answer": "If the report is in a personal workspace, it may lack traceability. Temporarily moving the workspace to Premium can help provide access.",
        "keywords": ["refresh", "power", "bi", "report", "access", "developer", "personal", "workspace", "premium", "traceability"]
    },
    {
        "question": "Why is my Power BI dashboard failing to refresh from Jira?",
        "answer": "The Power BI plugin in Jira was disabled due to issues. It has since been re-enabled.",
        "keywords": ["power", "bi", "dashboard", "refresh", "jira", "plugin", "disabled", "re-enabled"]
    },
    {
        "question": "What causes throttling in Power BI reports?",
        "answer": "Large dashboards (e.g., 710 MB) can cause capacity issues. Semantic model compression affects memory differently than disk size. Optimization and workspace quarantine may be needed.",
        "keywords": ["throttling", "power", "bi", "reports", "capacity", "large", "dashboards", "semantic", "model", "compression", "memory", "optimization", "quarantine"]
    },
    {
        "question": "What happens if a dataflow runs for more than 5 hours?",
        "answer": "It will be auto-cancelled. Removing the workspace from Premium temporarily can help resolve stuck refreshes.",
        "keywords": ["dataflow", "5", "hours", "auto-cancelled", "workspace", "premium", "stuck", "refreshes"]
    },
    {
        "question": "Why did my Sales Cockpit report fail to refresh?",
        "answer": "It was due to a gateway version update. The issue resolved after retrying.",
        "keywords": ["sales", "cockpit", "report", "refresh", "gateway", "version", "update", "retry"]
    },
    {
        "question": "Can users trigger a data refresh from the app?",
        "answer": "Technically yes, via Power Automate, but it's discouraged due to asynchronous behavior and potential overload (429 errors).",
        "keywords": ["users", "trigger", "refresh", "app", "power", "automate", "asynchronous", "overload", "429", "errors"]
    },
    {
        "question": "How can I display datetime in a specific timezone like Central Time?",
        "answer": "Convert everything to UTC upstream and only convert to local time at the final display step. Power BI lacks built-in timezone support.",
        "keywords": ["datetime", "timezone", "central", "time", "utc", "local", "display", "power", "bi", "support"]
    },
    {
        "question": "How can I cancel a dataflow refresh that won't stop?",
        "answer": "If regular cancellation fails, it will auto-fail after 24 hours. You can retry after that.",
        "keywords": ["cancel", "dataflow", "refresh", "stop", "24", "hours", "auto", "fail", "retry"]
    },
    {
        "question": "Why can't I see the Create App option in my workspace?",
        "answer": "Only one app per workspace is allowed. If an app exists, you can only update or unpublish it.",
        "keywords": ["create", "app", "workspace", "one", "per", "update", "unpublish"]
    },
    {
        "question": "Why does my API connection work in Power BI Desktop but not in a dataflow?",
        "answer": "API connections require a gateway. Multiple users can access it using the gateway owner's credentials.",
        "keywords": ["api", "connection", "power", "bi", "desktop", "dataflow", "gateway", "users", "credentials"]
    },
    {
        "question": "Is it safe for 30 users to use live Excel connections to a semantic model simultaneously?",
        "answer": "Not recommended during capacity overutilization. Use standard Excel exports instead. Live connections can request large result sets and strain resources.",
        "keywords": ["30", "users", "live", "excel", "connections", "semantic", "model", "simultaneously", "capacity", "overutilization", "exports", "strain", "resources"]
    },
    {
        "question": "How can I connect Hive server to Power BI?",
        "answer": "Use Cloudera drivers (not paid ones). Ensure TLS 1.2 or higher and a 64-bit System DSN.",
        "keywords": ["hive", "server", "power", "bi", "cloudera", "drivers", "tls", "dsn", "system", "connection", "connect"]
    }
]

def update_training_data():
    """Update training data with correct answers from PDF"""
    
    # Load current training data
    try:
        with open('data/training_data.json', 'r', encoding='utf-8') as f:
            current_data = json.load(f)
    except FileNotFoundError:
        current_data = []
    
    print(f"Current training data has {len(current_data)} entries")
    
    # Create a mapping of questions from PDF for easy lookup
    pdf_questions = {qa['question'].lower().strip(): qa for qa in pdf_qa_pairs}
    
    updated_count = 0
    added_count = 0
    
    # Update existing entries that match PDF questions
    for i, entry in enumerate(current_data):
        entry_question = entry['question'].lower().strip()
        
        # Check for exact or similar matches
        if entry_question in pdf_questions:
            pdf_entry = pdf_questions[entry_question]
            if entry['answer'] != pdf_entry['answer']:
                print(f"✅ UPDATING: {entry['question'][:50]}...")
                print(f"   OLD: {entry['answer'][:60]}...")
                print(f"   NEW: {pdf_entry['answer'][:60]}...")
                current_data[i] = pdf_entry
                updated_count += 1
            else:
                print(f"✓ CORRECT: {entry['question'][:50]}...")
        else:
            # Check for partial matches
            for pdf_q, pdf_entry in pdf_questions.items():
                if (len(entry_question) > 20 and len(pdf_q) > 20 and 
                    (entry_question in pdf_q or pdf_q in entry_question or
                     any(word in pdf_q for word in entry_question.split() if len(word) > 4))):
                    print(f"🔍 POSSIBLE MATCH:")
                    print(f"   Current: {entry['question']}")
                    print(f"   PDF:     {pdf_entry['question']}")
                    print(f"   Should these be the same? Manual review needed.")
                    break
    
    # Add new entries from PDF that don't exist in current data
    current_questions = {entry['question'].lower().strip() for entry in current_data}
    
    for pdf_qa in pdf_qa_pairs:
        if pdf_qa['question'].lower().strip() not in current_questions:
            print(f"➕ ADDING NEW: {pdf_qa['question'][:50]}...")
            current_data.append(pdf_qa)
            added_count += 1
    
    # Save updated training data
    with open('data/training_data_updated.json', 'w', encoding='utf-8') as f:
        json.dump(current_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 SUMMARY:")
    print(f"   Updated entries: {updated_count}")
    print(f"   Added new entries: {added_count}")
    print(f"   Total entries: {len(current_data)}")
    print(f"   Saved to: data/training_data_updated.json")
    
    return current_data

if __name__ == "__main__":
    print("Updating training data with correct answers from Amaan Q&A.pdf...")
    print("=" * 70)
    update_training_data()