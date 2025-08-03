# data_io.py
import sqlite3
import pandas as pd
from typing import List, Dict

DB_FILE = "stockflow.db"
STOCK_TABLE = "stock"
LOG_TABLE = "movement_log"


def create_tables():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(f"""
            CREATE TABLE IF NOT EXISTS {STOCK_TABLE} (
                Product TEXT PRIMARY KEY,
                Category TEXT,
                "Stock Level" INTEGER,
                "Min Stock Level" INTEGER,
                Location TEXT
            )
        """)
        c.execute(f"""
            CREATE TABLE IF NOT EXISTS {LOG_TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Product TEXT,
                "Movement Type" TEXT,
                Quantity INTEGER,
                Time TEXT
            )
        """)
        conn.commit()


def load_stock_data():
    create_tables()
    with sqlite3.connect(DB_FILE) as conn:
        df = pd.read_sql_query(f"SELECT * FROM {STOCK_TABLE}", conn)
        if df.empty:
            # Optional: load sample data if empty
            sample_data = {
                'Product': ['T-Shirt', 'Jeans', 'Jacket', 'Shoes', 'Hat'],
                'Category': ['Clothing', 'Clothing', 'Clothing', 'Footwear', 'Accessories'],
                'Stock Level': [50, 200, 30, 100, 75],
                'Min Stock Level': [40, 100, 20, 50, 60],
                'Location': ['A1', 'B2', 'C3', 'D4', 'E5']
            }
            df = pd.DataFrame(sample_data)
            save_stock_data(df)
        return df


def save_stock_data(df):
    create_tables()
    with sqlite3.connect(DB_FILE) as conn:
        df.to_sql(STOCK_TABLE, conn, if_exists="replace", index=False)


def load_movement_log():
    create_tables()
    with sqlite3.connect(DB_FILE) as conn:
        df = pd.read_sql_query(f"SELECT Product, `Movement Type`, Quantity, Time FROM {LOG_TABLE}", conn)
        return df.to_dict(orient="records")


def save_movement_log(log):
    if not log:
        return
    create_tables()
    df = pd.DataFrame(log)
    with sqlite3.connect(DB_FILE) as conn:
        df.to_sql(LOG_TABLE, conn, if_exists="append", index=False)


def find_product_by_barcode(barcode):
    # In the future, this will query a barcode table
    # For now, simulate with a dictionary
    barcode_map = {
        "123456789012": "T-Shirt",
        "987654321098": "Jeans",
        "456789012345": "Jacket"
    }
    return barcode_map.get(barcode, None)