# ui_components.py
import streamlit as st
import pandas as pd
import time

def scan_product():
    st.subheader("Scan Product (Barcode Input)")
    barcode = st.text_input("Scan or Enter Barcode")
    if barcode:
        st.session_state.barcode = barcode
        st.success(f"Barcode scanned: {barcode}")
        return barcode
    return None

def view_movement_log(movement_log):
    if movement_log:
        st.subheader("Movement Log")
        log_df = pd.DataFrame(movement_log)
        st.dataframe(log_df)

def display_current_stock_overview(df, key_suffix=""):
    st.subheader("Current Stock Overview")
    categories = ["All"] + list(df["Category"].unique())
    selected_category = st.selectbox("Filter by Category", categories, key=f"category_filter_overview_{key_suffix}")
    filtered_df = df if selected_category == "All" else df[df["Category"] == selected_category]

    for index, row in filtered_df.iterrows():
        if row["Stock Level"] < row["Min Stock Level"]:
            st.warning(f"{row['Product']} is below the minimum stock level!")

    st.dataframe(filtered_df[['Product', 'Category', 'Stock Level', 'Min Stock Level', 'Location']])


def log_stock_movement(df, movement_log):
    st.subheader("Log Stock Movement")
    product = st.selectbox("Select Product", df["Product"].tolist(), key="product_select")
    movement_type = st.selectbox(
        "Movement Type",
        ["New Stock Arrival", "Customer Return", "Customer Order", "Damaged", "Discrepancy", "Supplier Return"],
        key="movement_type"
    )
    quantity = st.number_input(
        "Quantity",
        min_value=1,
        max_value=500,
        value=1,
        key=f"quantity_input_{st.session_state.quantity_reset_counter}"
    )

    if st.button("Submit Movement"):
        delta = quantity if movement_type in ["New Stock Arrival", "Customer Return"] else -quantity
        df.loc[df["Product"] == product, "Stock Level"] += delta
        movement_log.append({
            "Product": product,
            "Movement Type": movement_type,
            "Quantity": quantity,
            "Time": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        st.success(f"Logged {movement_type} of {quantity} for {product}.")
        st.session_state.quantity_reset_counter += 1
        time.sleep(1)
        st.rerun()


def export_data(df, movement_log):
    st.subheader("Export Data")
    csv_stock = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Export Stock Data as CSV",
        data=csv_stock,
        file_name="stock_data.csv",
        mime="text/csv"
    )
    if movement_log:
        log_df = pd.DataFrame(movement_log)
        csv_log = log_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Export Movement Log as CSV",
            data=csv_log,
            file_name="movement_log.csv",
            mime="text/csv"
        )


def upload_data(df):
    st.subheader("Upload Stock Data")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        try:
            new_data = pd.read_csv(uploaded_file)
            required_columns = ["Product", "Category", "Stock Level", "Min Stock Level", "Location"]
            if not all(col in new_data.columns for col in required_columns):
                st.error("Uploaded file is missing required columns.")
                return
            st.session_state.df = new_data
            st.success("Data successfully uploaded and saved!")
            time.sleep(1)
            st.rerun()
        except Exception as e:
            st.error(f"Error processing the file: {e}")