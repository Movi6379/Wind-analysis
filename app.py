import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# Page configuration
st.set_page_config(page_title="2MW Solar & Wind Analysis", layout="wide")
st.title("☀️ 2MW Solar Plant: 7-Day Performance Dashboard")

# 1. Load Data
@st.cache_data
def load_data():
    # If your file is in the root of your GitHub, this is the name
    file_name = 'Generation_data.csv'
    
    # Safety Check: If file is missing, show a helpful message
    if not os.path.exists(file_name):
        st.error(f"⚠️ Error: '{file_name}' not found in the repository!")
        st.info("💡 Make sure you uploaded the CSV file (not just the zip) to your GitHub repo.")
        st.stop()

    df = pd.read_csv(file_name)
    
    # Recreating the missing timestamp (Assuming 5-second interval)
    df['Timestamp'] = pd.date_range(start='2024-01-01', periods=len(df), freq='5S')
    
    # Pre-calculations
    df['Temp_Delta'] = df['MODULE_TEMP'] - df['Amb_Temp']
    # Calculate Efficiency (avoiding division by zero)
    df['Efficiency'] = np.where(df['IRR (W/m2)'] > 10, (df['AC Power in Watts'] / (df['IRR (W/m2)'] * 2000)), 0)
    return df

df = load_data()

# --- THE REST OF YOUR CODE CONTINUES BELOW ---
# (Keep your Sidebar, Metrics, and Study columns exactly as they were)
