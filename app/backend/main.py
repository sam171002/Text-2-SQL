"""
main.py
-------
FastAPI backend for Text2SQL project.
Connects LLM (Gemini) + Azure SQL Database.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, List, Dict
import logging

# Import our services
from app.backend.services.llm_service import generate_sql_query
from app.backend.services.database_service import execute_sql_query

# Initialize FastAPI app
app = FastAPI(
    title="Text2SQL Backend API",
    description="Natural language to SQL query generator and executor using Gemini + Azure SQL.",
    version="1.0.0"
)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# -------------------------------
# 🩺 Health Check Route
# -------------------------------
@app.get("/")
def root():
    """Simple health check route."""
    return {"message": "✅ Text2SQL FastAPI backend is running!"}


# -------------------------------
# 📥 Input Model for /query
# -------------------------------
class QueryRequest(BaseModel):
    question: str


# -------------------------------
# 📤 Output Model for /query
# -------------------------------
class QueryResponse(BaseModel):
    sql_query: str
    results: List[Dict[str, Any]]


# -------------------------------
# 🚀 Main Endpoint: /query
# -------------------------------
@app.post("/query", response_model=QueryResponse)
def run_query(request: QueryRequest):
    """
    1. Generate SQL using Gemini.
    2. Execute SQL on Azure SQL DB.
    3. Return both query and results.
    """
    try:
        logging.info(f"Received query: {request.question}")

        # Step 1: Generate SQL
        sql_query = generate_sql_query(request.question)
        if not sql_query:
            raise HTTPException(status_code=400, detail="Failed to generate SQL query.")

        logging.info(f"Generated SQL: {sql_query}")

        # Step 2: Execute SQL
        result = execute_sql_query(sql_query)
        if not result or "rows" not in result or "columns" not in result:
            raise HTTPException(status_code=500, detail="Failed to execute SQL or no results returned.")

        # Step 3: Format Results
        rows = result["rows"]
        columns = result["columns"]
        formatted_results = [dict(zip(columns, row)) for row in rows]

        logging.info(f"Returning {len(formatted_results)} rows.")
        return QueryResponse(sql_query=sql_query, results=formatted_results)

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Unhandled error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
