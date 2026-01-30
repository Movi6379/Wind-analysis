import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page configuration
st.set_page_config(page_title="2MW Solar & Wind Analysis", layout="wide")
st.title("☀️ 2MW Solar Performance & Wind-Cooling Dashboard")

# 1. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('Generation_data.csv.zip')
    # Recreating the missing timestamp (Assuming 5-second interval)
    df['Timestamp'] = pd.date_range(start='2024-01-01', periods=len(df), freq='5S')
    
    # Pre-calculations
    df['Temp_Delta'] = df['MODULE_TEMP'] - df['Amb_Temp']
    # Calculate Efficiency (avoiding division by zero)
    df['Efficiency'] = np.where(df['IRR (W/m2)'] > 10, (df['AC Power in Watts'] / (df['IRR (W/m2)'] * 2000)), 0)
    return df

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Data")
day_filter = st.sidebar.slider("Select Data Range (Rows)", 0, len(df), (0, 10000))
display_df = df.iloc[day_filter[0]:day_filter[1]]

# --- TOP METRICS ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Peak AC Power", f"{df['AC Power in Watts'].max()/1000:.2f} kW")
m2.metric("Avg Wind Speed", f"{df['WIND_Speed'].mean():.2f} m/s")
m3.metric("Max Module Temp", f"{df['MODULE_TEMP'].max():.1f} °C")
m4.metric("Avg Irradiance", f"{df['IRR (W/m2)'].mean():.1f} W/m²")

# --- STUDY 1 & 2 ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Wind-Cooling Effect")
    fig1 = px.scatter(display_df, x="WIND_Speed", y="Temp_Delta", color="MODULE_TEMP",
                     title="Wind Speed vs. Temperature Delta (Module - Ambient)")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("2. Temperature-Corrected Efficiency")
    fig2 = px.scatter(display_df, x="MODULE_TEMP", y="Efficiency", color="IRR (W/m2)",
                     title="Efficiency vs. Module Temperature")
    st.plotly_chart(fig2, use_container_width=True)

# --- STUDY 3 & 4 ---
col3, col4 = st.columns(2)

with col3:
    st.subheader("3. 3-Phase Load Balance")
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=display_df['Timestamp'], y=display_df['AC Ir in Amps'], name='Phase R'))
    fig3.add_trace(go.Scatter(x=display_df['Timestamp'], y=display_df['AC Iy in Amps'], name='Phase Y'))
    fig3.add_trace(go.Scatter(x=display_df['Timestamp'], y=display_df['AC Ib in Amps'], name='Phase B'))
    fig3.update_layout(title="3-Phase AC Current Comparison")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("4. Solar Power Curve")
    fig4 = px.scatter(display_df, x="IRR (W/m2)", y="AC Power in Watts", 
                     title="Power Curve (Irradiance vs. AC Power)")
    st.plotly_chart(fig4, use_container_width=True)

# --- STUDY 5 & 6 ---
col5, col6 = st.columns(2)

with col5:
    st.subheader("5. Thermal Regression Visual")
    fig5 = px.density_heatmap(display_df, x="Amb_Temp", y="MODULE_TEMP", z="WIND_Speed",
                             title="Heatmap: Ambient vs. Module Temp by Wind")
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.subheader("6. DC Current vs. AC Power")
    fig6 = px.line(display_df, x="DC Current in Amps", y="AC Power in Watts",
                  title="Inverter Performance (DC Input vs AC Output)")
    st.plotly_chart(fig6, use_container_width=True)
