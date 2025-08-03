# visuals.py
import streamlit as st
import plotly.express as px
import pandas as pd


def visualise_stock_trends(df, movement_log):
    st.subheader("Stock Levels and Trends")

    col1, col2 = st.columns(2)

    # Bar chart
    fig = px.bar(
        df,
        x="Product",
        y="Stock Level",
        color="Category",
        title="Stock Levels by Product and Category"
    )
    with col1:
        st.plotly_chart(fig, use_container_width=True)

    # Line chart (if movement log exists)
    if movement_log:
        log_df = pd.DataFrame(movement_log)
        fig2 = px.line(
            log_df,
            x="Time",
            y="Quantity",
            color="Product",
            title="Historical Stock Movements Over Time"
        )
        with col2:
            st.plotly_chart(fig2, use_container_width=True)