# main.py
import streamlit as st
import pandas as pd


from ui_components import scan_product


# Import necessary functions from other modules
from ui_components import (
    display_current_stock_overview,
    log_stock_movement,
    export_data,
    upload_data,
    view_movement_log,
    scan_product   
)

from data_io import load_stock_data, save_stock_data, save_movement_log, load_movement_log
from ui_components import (
    display_current_stock_overview,
    log_stock_movement,
    export_data,
    upload_data
)
from visuals import visualise_stock_trends

# Initialize session state
if "quantity_reset_counter" not in st.session_state:
    st.session_state.quantity_reset_counter = 0

if 'df' not in st.session_state:
    st.session_state.df = load_stock_data()

if 'movement_log' not in st.session_state:
    st.session_state.movement_log = load_movement_log()

# App UI
st.title("StockFlow - Small Retailers")

scan_product() 
display_current_stock_overview(st.session_state.df, key_suffix="main")
log_stock_movement(st.session_state.df, st.session_state.movement_log)
view_movement_log(st.session_state.movement_log) 
export_data(st.session_state.df, st.session_state.movement_log)
visualise_stock_trends(st.session_state.df, st.session_state.movement_log)
upload_data(st.session_state.df)

# Save data after every interaction
save_stock_data(st.session_state.df)
save_movement_log(st.session_state.movement_log)