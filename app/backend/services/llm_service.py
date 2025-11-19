"""
llm_service.py (v4)
-------------------
Handles communication with Gemini API for Text-to-SQL generation.
Includes SQL validation, optimization, and retry mechanism.
"""

import os
import re
import json
import logging
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# ---------------------- UTILITY FUNCTIONS ----------------------

def load_schema(schema_path="data/schema_info.json"):
    """Load database schema from JSON file."""
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema file not found at {schema_path}")
    with open(schema_path, "r") as f:
        return json.load(f)


def build_prompt(user_query: str, schema: dict) -> str:
    """Builds a structured prompt for Gemini to generate SQL."""
    schema_text = json.dumps(schema, indent=2)
    prompt = f"""
You are an expert SQL generator.
Given the following database schema and user question, generate a valid SQL query for Microsoft SQL Server (T-SQL).

--- DATABASE SCHEMA ---
{schema_text}

--- USER QUESTION ---
{user_query}

Rules:
1. Use correct table and column names as per the schema.
2. Return only pure SQL (no explanations, no markdown, no commentary).
3. Ensure syntax is valid SQLite.
4. If user did not specify a limit, append "TOP 10" right after SELECT.


Return only the SQL query, nothing else.
"""
    return prompt


def clean_sql_output(raw_text: str) -> str:
    """
    Cleans Gemini output to extract pure SQL.
    Handles markdown, explanations, prefixes like 'sqlite'.
    """
    if not raw_text:
        return ""

    text = raw_text.strip()

    # Remove markdown and language identifiers
    text = re.sub(r"```(sql|sqlite)?", "", text, flags=re.IGNORECASE)
    text = text.replace("```", "").replace("SQL Query:", "").replace("Generated SQL:", "")

    # Extract portion starting with SELECT or WITH
    match = re.search(r"(SELECT|WITH)\s+.*", text, flags=re.IGNORECASE | re.DOTALL)
    if match:
        text = match.group(0)
    else:
        text = text.strip()

    # Remove extra whitespace and trailing semicolons
    text = text.strip().rstrip(";").strip()

    # Remove unwanted "sqlite" prefix
    text = re.sub(r"^sqlite\s*", "", text, flags=re.IGNORECASE).strip()

    return text


# ---------------------- VALIDATOR ----------------------

def validate_sql_query(sql_query: str) -> bool:
    """
    Validates that the SQL query is safe and syntactically reasonable.
    """
    try:
        sql_query = sql_query.strip()

        # Basic structure
        if not re.match(r"^\s*(SELECT|WITH)\s+.+\s+FROM\s+.+", sql_query, re.IGNORECASE | re.DOTALL):
            logging.warning("⚠️ SQL does not start with SELECT/WITH or lacks FROM clause.")
            return False

        # Forbidden keywords
        forbidden = ["delete", "update", "insert", "drop", "alter"]
        if any(word in sql_query.lower() for word in forbidden):
            logging.warning("⚠️ Forbidden SQL operation detected.")
            return False

        logging.info("✅ SQL validation successful.")
        return True

    except Exception as e:
        logging.warning(f"⚠️ SQL validation failed: {e}")
        return False


# ---------------------- OPTIMIZER ----------------------

def optimize_sql_query(sql_query: str) -> str:
    """Adds LIMIT clause if missing, removes dangerous operations."""
    query = sql_query.strip().rstrip(";")

    # Skip if it's unsafe
    forbidden = ["delete", "update", "insert", "drop", "alter"]
    if any(word in query.lower() for word in forbidden):
        logging.warning("⚠️ Dangerous SQL detected. Ignoring.")
        return ""

    # Add LIMIT 10 if missing
    if re.match(r"(?i)^select\s+(?!top\s+\d+)", query):
        # Insert TOP 10 after SELECT if not already there
        query = re.sub(r"(?i)^select\s+", "SELECT TOP 10 ", query, count=1)

    return query + ";"


# ---------------------- CORE FUNCTION ----------------------

def generate_sql_query(user_query: str, schema_path="data/schema_info.json", max_retries=3) -> str:
    """
    Main function: generates, cleans, validates, and optimizes SQL with retries.
    """
    schema = load_schema(schema_path)
    model = genai.GenerativeModel("gemini-2.5-flash")  # stable version

    for attempt in range(1, max_retries + 1):
        logging.info("🧠 Attempt %d/%d for query: %s", attempt, max_retries, user_query)

        try:
            prompt = build_prompt(user_query, schema)
            response = model.generate_content(prompt)
            raw_sql = response.text.strip() if hasattr(response, "text") else str(response)
            sql_query = clean_sql_output(raw_sql)

            if not sql_query:
                logging.warning("⚠️ Empty SQL generated.")
                continue

            sql_query = optimize_sql_query(sql_query)
            if not sql_query:
                logging.warning("⚠️ Unsafe SQL skipped.")
                continue

            if validate_sql_query(sql_query):
                logging.info(f"✅ Final Valid SQL:\n{sql_query}")
                return sql_query

            logging.warning("⚠️ Invalid SQL generated, retrying...")

        except Exception as e:
            logging.error(f"❌ Error in attempt {attempt}: {e}")

    logging.error("❌ All retry attempts failed to generate valid SQL.")
    return None
