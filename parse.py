from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd
import json

class TableProcessor:
    def __init__(self, api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=api_key
        )
    
    def generate_analysis_prompt(self, table_data: List[Dict[str, Any]], context_text: str) -> str:
        """Creates a prompt for the LLM to strictly enhance the table data."""
        table_str = json.dumps(table_data, indent=2)
        return f"""You are an advanced AI specializing in refining structured data from web pages. Your task is to always generate or enhance a table using the provided data while strictly adhering to these instructions:

1. Identify useful and relevant data: Extract key information and remove any redundant, misleading, or irrelevant content.
2. Enhance the table: Improve categorization, infer missing but valuable information, and restructure the data for better readability.
3. Always generate a valid table: If no structured table exists, construct one based on context and extracted key-value pairs.
4. No raw text output: Your response should be a structured JSON object containing only the enhanced table data.
5. Always generate a table in context of the data provided the tables need to be properly labeled and should make sense to a human readable format.

Input Table Data:
{table_str}

Context:
{context_text}

Provide your response as a JSON object in this format:
{{
    "enhanced_table": {{
        "headers": ["column1", "column2", ...],
        "data": [
            {{"column1": "value1", "column2": "value2", ...}},
            ...
        ]
    }}
}}"""

    def enhance_table(self, table_data: List[Dict[str, Any]], context_text: str) -> Dict[str, Any]:
        """Processes table data through the LLM to create an enhanced version."""
        prompt = self.generate_analysis_prompt(table_data, context_text)
        
        try:
            response = self.llm.invoke(prompt)
            enhanced_data = json.loads(response.content)
            return enhanced_data
        except Exception as e:
            return {
                "error": f"Failed to process table: {str(e)}",
                "enhanced_table": {
                    "headers": ["Generated Column 1", "Generated Column 2"],
                    "data": []
                }
            }

def process_scraped_data(structured_data: Dict[str, Any], api_key: str) -> Dict[str, Any]:
    """Processes all scraped data and ensures a table is always generated."""
    processor = TableProcessor(api_key)
    enhanced_tables = []
    
    if "tables" in structured_data and "text_summary" in structured_data:
        for table in structured_data.get("tables", []):
            enhanced_table = processor.enhance_table(
                table.get("table_data", []),
                structured_data["text_summary"]
            )
            enhanced_tables.append(enhanced_table)
    
    if not enhanced_tables:
        enhanced_tables.append(processor.enhance_table([], structured_data.get("text_summary", "")))
    
    return {"enhanced_tables": enhanced_tables}
