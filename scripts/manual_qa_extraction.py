"""
Manual Q&A extraction based on observed PDF structure
"""

import json
import os

def create_qa_from_pdf():
    """Manually create Q&A data based on the PDF content we observed"""
    
    qa_pairs = [
        {
            "question": "Why is there a discrepancy between the number shown on screen and the exported data from Power BI?",
            "answer": "The issue arises when attributes are added to the visualization. Removing them aligns the data. Exported CSV values are static and not bound by model logic, so summing them directly may be unsafe.",
            "keywords": ["power", "bi", "export", "data", "discrepancy", "csv", "visualization", "attributes"]
        },
        {
            "question": "How can I connect Power BI Server to Azure Databricks?",
            "answer": "Use the 'Azure Databricks' connector (not 'Databricks') via the Colo-1 Power Platform gateway. Follow the instructions on the Power BI Gateway SharePoint page.",
            "keywords": ["power", "bi", "server", "azure", "databricks", "connector", "gateway", "connection"]
        },
        {
            "question": "Why does my Power BI report fail during scheduled refresh but works manually?",
            "answer": "It could be due to dynamic file usage (e.g., daily Excel files). Ensure the file format (e.g., XLSX) and hosting (e.g., SharePoint) are consistent and supported.",
            "keywords": ["power", "bi", "refresh", "scheduled", "fail", "excel", "sharepoint", "file", "format"]
        },
        {
            "question": "How can I refresh a Power BI report if I don't have access or know the developer?",
            "answer": "If the report is in a personal workspace, it may lack traceability. Temporarily moving the workspace to Premium can help provide access.",
            "keywords": ["power", "bi", "refresh", "access", "developer", "workspace", "premium", "personal"]
        },
        {
            "question": "Why is my Power BI dashboard failing to refresh from Jira?",
            "answer": "The Power BI plugin in Jira was disabled due to issues. It has since been re-enabled.",
            "keywords": ["power", "bi", "jira", "plugin", "dashboard", "refresh", "disabled", "enabled"]
        },
        {
            "question": "What causes throttling in Power BI reports?",
            "answer": "Large dashboards (e.g., 710 MB) can cause capacity issues. Semantic model compression affects memory differently than disk size. Optimization and workspace quarantine may be needed.",
            "keywords": ["power", "bi", "throttling", "capacity", "large", "dashboard", "semantic", "model", "optimization"]
        },
        {
            "question": "What happens if a dataflow runs for more than 5 hours?",
            "answer": "It will be auto-cancelled. Removing the workspace from Premium temporarily can help resolve stuck refreshes.",
            "keywords": ["dataflow", "5", "hours", "auto", "cancelled", "workspace", "premium", "stuck", "refresh"]
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
            "keywords": ["datetime", "timezone", "central", "time", "utc", "local", "display", "power", "bi"]
        },
        {
            "question": "How can I cancel a dataflow refresh that won't stop?",
            "answer": "If regular cancellation fails, it will auto-fail after 24 hours. You can retry after that.",
            "keywords": ["cancel", "dataflow", "refresh", "stop", "24", "hours", "auto", "fail", "retry"]
        },
        {
            "question": "Why can't I see the Create App option in my workspace?",
            "answer": "Only one app per workspace is allowed. If an app exists, you can only update or unpublish it.",
            "keywords": ["create", "app", "option", "workspace", "one", "per", "update", "unpublish"]
        },
        {
            "question": "Why does my API connection work in Power BI Desktop but not in a dataflow?",
            "answer": "API connections require a gateway. Multiple users can access it using the gateway owner's credentials.",
            "keywords": ["api", "connection", "power", "bi", "desktop", "dataflow", "gateway", "users", "credentials"]
        },
        {
            "question": "Is it safe for 30 users to use live Excel connections to a semantic model simultaneously?",
            "answer": "Live connections should be evaluated for capacity impact. Consider the semantic model's capacity and potential performance implications with multiple concurrent users.",
            "keywords": ["30", "users", "live", "excel", "connections", "semantic", "model", "simultaneously", "capacity", "performance"]
        },
        {
            "question": "How do I resolve Hive Server connection issues?",
            "answer": "Check gateway connectivity, verify Hive Server credentials, and ensure proper network configuration. Review gateway logs for specific error messages.",
            "keywords": ["hive", "server", "connection", "issues", "gateway", "connectivity", "credentials", "network", "logs"]
        }
    ]
    
    return qa_pairs

def main():
    """Main function to create and save Q&A data"""
    qa_pairs = create_qa_from_pdf()
    
    print(f"Created {len(qa_pairs)} Q&A pairs from PDF content")
    
    # Display first few Q&A pairs
    print("\nSample Q&A pairs:")
    for i, qa in enumerate(qa_pairs[:3]):
        print(f"\n{i+1}. Question: {qa['question']}")
        print(f"   Answer: {qa['answer'][:100]}...")
        print(f"   Keywords: {qa['keywords']}")
    
    # Save extracted data
    output_file = os.path.join(os.path.dirname(__file__), 'extracted_qa.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(qa_pairs, f, indent=2, ensure_ascii=False)
    
    print(f"\nQ&A data saved to: {output_file}")
    return qa_pairs

if __name__ == "__main__":
    main()