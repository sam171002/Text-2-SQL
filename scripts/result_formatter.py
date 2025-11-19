# app/backend/utils/result_formatter.py
"""
Result formatter utilities for Text2SQL project.

Functions:
- rows_to_dataframe(result): converts {"columns": [...], "rows": [...]} to pandas.DataFrame
- print_table(result, max_rows=20): prints pretty table to terminal using tabulate
- plot_bar_from_groupby(df, x_col, y_col, title): returns a plotly figure for bar plots
- download_csv_bytes(df): returns CSV bytes for Streamlit download button
"""

from typing import Dict, Any
import pandas as pd
from tabulate import tabulate
import plotly.express as px
import io

def rows_to_dataframe(result: Dict[str, Any]) -> pd.DataFrame:
    """
    Convert query result dictionary to pandas DataFrame.
    result expected: {"columns": [...], "rows": [...]}
    Rows may be pyodbc.Row or tuples; handle both.
    """
    if result is None:
        return pd.DataFrame()

    cols = result.get("columns", [])
    rows = result.get("rows", [])

    # Convert pyodbc.Row to tuple if necessary
    parsed_rows = []
    for r in rows:
        # if row is pyodbc.Row, it's indexable; convert to tuple
        try:
            parsed_rows.append(tuple(r))
        except Exception:
            parsed_rows.append(tuple(r))

    df = pd.DataFrame(parsed_rows, columns=cols)
    return df


def print_table(result: Dict[str, Any], max_rows: int = 20):
    """
    Nicely print the result table to the terminal using tabulate.
    """
    df = rows_to_dataframe(result)
    if df.empty:
        print("No results to display.")
        return

    display_df = df.head(max_rows)
    print(tabulate(display_df, headers='keys', tablefmt='psql', showindex=False))
    if len(df) > max_rows:
        print(f"... ({len(df) - max_rows} more rows) ...")


def plot_bar_from_groupby(df: pd.DataFrame, x_col: str = None, y_col: str = None, title: str = None):
    """
    Create a bar chart from a DataFrame.
    If x_col/y_col not provided and df has two columns, use first as x and second as y.
    Returns a plotly.graph_objects.Figure.
    """
    if df is None or df.empty:
        raise ValueError("DataFrame is empty")

    if x_col is None or y_col is None:
        if len(df.columns) >= 2:
            x_col = df.columns[0] if x_col is None else x_col
            y_col = df.columns[1] if y_col is None else y_col
        else:
            raise ValueError("Cannot infer columns for plotting: DataFrame has <2 columns")

    title = title or f"{y_col} by {x_col}"

    # Try to coerce y to numeric
    df_plot = df.copy()
    df_plot[y_col] = pd.to_numeric(df_plot[y_col], errors='coerce').fillna(0)

    fig = px.bar(df_plot, x=x_col, y=y_col, title=title, labels={x_col: x_col, y_col: y_col})
    fig.update_layout(xaxis_tickangle=-45, margin=dict(t=50, b=150))
    return fig


def download_csv_bytes(df: pd.DataFrame) -> bytes:
    """
    Return CSV bytes of the given DataFrame, for Streamlit download.
    """
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")
