import streamlit as st
import pandas as pd 
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import json
import os
import warnings
import streamlit.components.v1 as com
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import matplotlib.pyplot as plt

st.set_page_config(page_title="F1 Dashboard", page_icon=":bar_chart:", layout="wide")
st.title(" :bar_chart: F1 Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

with open('./style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}<style>', unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload a file", type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding = "ISO-8859-1")
else:
    os.chdir(r"C:\Users\nplam\F1 simulator")
    df = pd.read_csv('f1_2022_juul_2.csv', encoding = "ISO 8859-1")
    
car_type = {"Ferrari":"carId", "Mercedes":"carId", "Aston Martin":"carId", "Alfa Romeo":"carId", "Alpha Tauri":"carId", "Alpine":"carId", "Haas":"carId", "McLaren":"carId", "Red Bull":"carId", "Williams":"carId"}
types = ["Mean","Absolute","Median","Maximum","Minimum"]
label_attr_dict_teams = {"Velocity":"velocity_X", "G Force":"gforce_X", "Round per Minute":"rpm"}

st.dataframe(df)

st.sidebar.header("Filter Data")

selected_lap = st.sidebar.text_input("Enter Lap Number")    

try:
    selected_lap = int(selected_lap)
except ValueError:
    selected_lap = None

if selected_lap is not None:
    filtered_data = df[df['lapNum'] == selected_lap]
else:
    filtered_data = pd.DataFrame() 

def read_lap_time(file):
    data = pd.read_csv(file)
    return data

def plot_x_per_team(attr,measure): 
    rc = {'figure.figsize':(8,4.5),
          'axes.facecolor':'#0e1117',
          'axes.edgecolor': '#0e1117',
          'axes.labelcolor': 'white',
          'figure.facecolor': '#0e1117',
          'patch.edgecolor': '#0e1117',
          'text.color': 'white',
          'xtick.color': 'white',
          'ytick.color': 'white',
          'grid.color': 'grey',
          'font.size' : 8,
          'axes.labelsize': 12,
          'xtick.labelsize': 8,
          'ytick.labelsize': 12}
    
    plt.rcParams.update(rc)
    fig, ax = plt.subplots() 

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
        fig = px.pie(filtered_data, values = "rpm", names = "lap_number", hole = 0.5, title = 'velocity over lap number' )
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

com.iframe("https://lottie.host/?file=5297ccb9-c5df-4574-beed-b1654ebe58bd/2BE3pTuQMo.json")

def main():
    st.markdown("### Control Panel - Speed")
    speed_value = st.slider("Speed", min_value=0, max_value=40000, value=27859, step=1)  # Scale up by 1000
    formatted_speed = speed_value / 1000  # Scale down by 1000 for display
    st.write(f"Current Speed: {formatted_speed:.3f} 1000km/h")

if __name__ == "__main__":
    main()

def main():
    st.markdown("### Fuel Level")
    fuel_value = st.slider("Fuel Level", min_value=0, max_value=100, value=76, step=1)
    st.progress(fuel_value)

if __name__ == "__main__":
    main()

lap_filter = st.selectbox("Select the lap", pd.unique(df["lapNum"]))
df = df[df["lapNum"] == lap_filter]

row4_spacer1, row4_1, row4_spacer2 = st.columns((.2, 7.1, .2))
with row4_1:
    st.subheader('Analysis per Team')
row5_spacer1, row5_1, row5_spacer2, row5_2, row5_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
with row5_1:
    st.markdown('Investigate a variety of stats for each team. Which team do you want to see and which KPI would you want to be displayed?')    
    plot_x_per_team_selected = st.selectbox ("Which attribute do you want to analyze?", list(label_attr_dict_teams.keys()), key = 'attribute_team')
    plot_x_per_team_type = st.selectbox ("Which measure do you want to analyze?", types, key = 'measure_team')
with row5_2:
    uploaded_files = st.sidebar.file_uploader("Upload CSV files", accept_multiple_files=True)

if len(uploaded_files) == 2:
    lap_time_data = [read_lap_time(file) for file in uploaded_files]

    st.write("## Comparison")

    plt.figure(figsize=(8, 6))
    for i, data in enumerate(lap_time_data):
        lap_time_column = st.selectbox(f"Select Lap Time Column from File {i+1}", data.columns)
        plt.plot(data[lap_time_column], label=f'Files {i+1}')

    plt.xlabel('')
    plt.ylabel('')
    plt.legend()
    st.pyplot(plt)
elif len(uploaded_files) > 2:
    st.write("Please upload only two CSV files to compare")
else:
    st.write("Please upload two CSV files to compare")
    plot_x_per_team(plot_x_per_team_selected, plot_x_per_team_type)
