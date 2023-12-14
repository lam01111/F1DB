import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="F1 Dashboard", page_icon=":bar_chart:", layout="wide")
st.title(" :bar_chart: F1 Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

with open('./style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}<style>', unsafe_allow_html=True)

def read_lap_time(file):
    data = pd.read_csv(file)
    return data

st.title('Comparison of KPIs')

uploaded_files = st.sidebar.file_uploader("Upload CSV files", accept_multiple_files=True)

if len(uploaded_files) == 2:
    lap_time_data = [read_lap_time(file) for file in uploaded_files]

    plt.figure(figsize=(8, 6))
    for i, data in enumerate(lap_time_data):
        lap_time_column = st.selectbox(f"Select from File {i+1}", data.columns)
        plt.plot(data[lap_time_column], label=f'Files {i+1}')

    plt.xlabel('')
    plt.ylabel('')
    plt.legend()
    st.pyplot(plt)
elif len(uploaded_files) > 2:
    st.write("Please upload only two CSV files to compare")
else:
    st.write("Please upload two CSV files to compare")
