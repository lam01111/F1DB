import streamlit as st
import pandas as pd 
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import json
import os
import warnings
import streamlit.components.v1 as com

st.set_page_config(page_title="F1 Dashboard", page_icon=":bar_chart:", layout="wide")
st.title(" :bar_chart: F1 Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

with open('./style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}<style>', unsafe_allow_html=True)

def read_lap_time(file):
    data = pd.read_csv(file)
    return data

st.sidebar.header("Dashboard")
fl = st.sidebar.file_uploader(":file_folder: Upload a file for the dashboard", type=(["csv","txt","xlsx","xls"]))

selected_lap = st.sidebar.text_input("Enter Lap Number")  

if fl is not None:
    df = pd.read_csv(fl)

st.write(df)

try:
    selected_lap = int(selected_lap)
except ValueError:
    selected_lap = None

if selected_lap is not None:
    filtered_data = df[df['lapNum'] == selected_lap]
else:
    filtered_data = pd.DataFrame() 

col1, col2, = st.columns((2))

if not filtered_data.empty: 

    with col1:
        fig = px.bar(filtered_data, x = 'lap_distance', y = 'rpm',  title='RPM Over Lap Distance')
        fig.update_layout(
            title_text="RPM Over Lap Distance",
            xaxis_title="Lap Distance",
            yaxis_title="RPM"
        )
        st.plotly_chart(fig)

    with col2:
        fig = px.pie(filtered_data, values = "rpm", names = "lap_number", hole = 0.5, title = 'RPM over lap number' )
        fig.update_traces(text = filtered_data["lap_number"], textposition = "outside")
        st.plotly_chart(fig)    

velocity_X, lap_time, gear, rpm, wheel_speed_0, Averagespeed = st.tabs(["Velocity", "Lap Time", "Gear", "Rpm", "Wheel speed", "Average Speed"])

with velocity_X:
    st.line_chart(df['velocity_X'])

with lap_time:
    st.line_chart(df['lap_time'])

with gear:
    st.line_chart(df['gear'])

with rpm:
    st.line_chart(df['rpm'])

with wheel_speed_0:
    st.line_chart(df['wheel_speed_0'])

with Averagespeed:
    df['velocity_X_kmh'] = df['velocity_X'] * 3.6
    Averagespeed = df.groupby(by="lapNum")["velocity_X_kmh"].mean()
    fig.update_layout(title_text = ("Average speed"), xaxis_title="Km/h", yaxis_title="Lap")
    st.line_chart(Averagespeed)

st.title("Comparison between 2 files")

uploaded_files = st.sidebar.file_uploader("Upload 2 files to compare", accept_multiple_files=True)

if len(uploaded_files) == 2:
    lap_time_data = [read_lap_time(file) for file in uploaded_files]

    plt.figure(figsize=(8, 6))
    for i, data in enumerate(lap_time_data):
        lap_time_column = st.selectbox(f"Select from File {i+1}", data.columns)
        plt.plot(data[lap_time_column], label=f'File {i+1}')

    plt.xlabel('')
    plt.ylabel('')
    plt.legend()
    st.pyplot(plt)
elif len(uploaded_files) > 2:
    st.write("Please upload only two CSV files to compare")
else:
    st.write("Please upload two CSV files to compare")
