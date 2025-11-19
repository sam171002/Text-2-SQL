import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import streamlit as st
import requests
import pandas as pd
from scripts.result_formatter import plot_bar_from_groupby, download_csv_bytes

API_URL = "http://127.0.0.1:8000/query"

st.set_page_config(page_title="Data Explorer", layout="wide")
st.title("🧬 Data Explorer (Text2SQL)")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Reset chat
if st.button("🧹 Start New Chat"):
    st.session_state.chat_history = []
    st.rerun()

# Display chat messages
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
user_query = st.chat_input("Ask a question about your cancer dataset...")

if user_query:
    # Show user message
    st.chat_message("user").markdown(user_query)

    with st.spinner("⏳ Thinking..."):
        try:
            response = requests.post(API_URL, json={
                "question": user_query,
                "chat_history": st.session_state.chat_history
            })

            if response.status_code == 200:
                data = response.json()
                sql_query = data.get("sql_query", "")
                results = data.get("results", [])

                # Show assistant message
                assistant_response = f"Here’s the SQL I generated:\n```sql\n{sql_query}\n```"
                if results:
                    df = pd.DataFrame(results)
                    assistant_response += f"\nReturned **{len(df)} rows**."

                st.chat_message("assistant").markdown(assistant_response)

                # Update history
                st.session_state.chat_history.append({"role": "user", "content": user_query})
                st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

                # Show results
                if results:
                    st.subheader("📊 Query Results")
                    st.dataframe(df, use_container_width=True)

                    try:
                        if len(df.columns) >= 2:
                            x_col, y_col = df.columns[:2]
                            fig = plot_bar_from_groupby(df, x_col, y_col, f"{y_col} by {x_col}")
                            st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.warning(f"⚠️ Could not generate chart: {e}")

                    csv_bytes = download_csv_bytes(df)
                    st.download_button(
                        label="⬇️ Download Results as CSV",
                        data=csv_bytes,
                        file_name="query_results.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No data returned for this query.")
            else:
                st.chat_message("assistant").error(f"Backend Error: {response.status_code}")
                st.text(response.text)

        except Exception as e:
            st.chat_message("assistant").error(f"❌ Failed to connect to backend: {e}")