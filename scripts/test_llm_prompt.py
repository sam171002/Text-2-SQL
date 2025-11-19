# scripts/test_llm_prompt.py
"""
Interactive test script for the Text2SQL pipeline, now with pretty output and plot.
"""

from app.backend.services.llm_service import generate_sql_query
from app.backend.services.database_service import execute_sql_query
from scripts.result_formatter import rows_to_dataframe, print_table, plot_bar_from_groupby
import webbrowser
import tempfile
import streamlit as st  # optional import if you later run the streamlit snippet

if __name__ == "__main__":
    user_query = input("Enter your natural language question: ")

    sql_query = generate_sql_query(user_query)
    print("\nGenerated SQL Query:\n", sql_query)

    if sql_query:
        print("\nExecuting on Azure SQL Database...")
        result = execute_sql_query(sql_query)

        if result:
            print("\n✅ Query Results (terminal):")
            print_table(result, max_rows=15)

            # Convert to DataFrame
            df = rows_to_dataframe(result)

            # If it's a simple group/count result (2 columns), create a bar chart and save as html
            if df.shape[1] >= 2:
                try:
                    fig = plot_bar_from_groupby(df)
                    # Save plotly figure to a temporary HTML and open in browser (quick local demo)
                    tmp = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
                    fig.write_html(tmp.name)
                    print(f"\n📈 Bar chart saved to {tmp.name} — opening in browser...")
                    webbrowser.open("file://" + tmp.name)
                except Exception as e:
                    print("Could not create chart:", e)
        else:
            print("❌ Failed to execute SQL query on Azure DB.")
