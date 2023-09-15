import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df['Time of Measurement'] = pd.to_datetime(df['Time of Measurement'])
    df['Fat (kg)'] = (df['Body Fat(%)'] / 100) * df['Weight(kg)']
    df['30-day MA Weight'] = df['Weight(kg)'].rolling(window=30).mean()
    df['90-day Exponential Smoothing Weight'] = df['Weight(kg)'].ewm(span=90).mean()
    df['30-day MA Body Fat(%)'] = df['Body Fat(%)'].rolling(window=30).mean()
    df['90-day Exponential Smoothing Body Fat(%)'] = df['Body Fat(%)'].ewm(span=90).mean()
    df['30-day MA Fat (kg)'] = df['Fat (kg)'].rolling(window=30).mean()
    df['90-day Exponential Smoothing Fat (kg)'] = df['Fat (kg)'].ewm(span=90).mean()
    return df

st.title('Weight and Health Stats Analysis')

uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    df = load_data(uploaded_file)

    # Sidebar for Weight Analysis
    st.sidebar.header('Settings for Weight Analysis')
    selected_metrics_weight = st.sidebar.multiselect(
        'Select metrics to plot', 
        options=['Weight(kg)', 'Fat (kg)', '30-day MA Weight', '90-day Exponential Smoothing Weight'],
        default=['Weight(kg)', '30-day MA Weight', '90-day Exponential Smoothing Weight']
    )

    # Main Weight Analysis
    st.header('Weight Analysis')
    fig_weight = go.Figure()
    for metric in selected_metrics_weight:
        if metric in ['Weight(kg)', 'Fat (kg)']:
            fig_weight.add_trace(go.Scatter(x=df['Time of Measurement'], y=df[metric], mode='markers', opacity=0.5, name=metric))
        else:
            fig_weight.add_trace(go.Scatter(x=df['Time of Measurement'], y=df[metric], mode='lines', name=metric))
    fig_weight.update_layout(xaxis_title="Date", height=600)
    st.plotly_chart(fig_weight)
    
    # Sidebar for Body Fat Analysis
    st.sidebar.header('Settings for Body Fat Analysis')
    body_fat_choice = st.sidebar.radio("Choose metric type for Body Fat Analysis", ['Percentage (%)', 'Kilograms (kg)'])

    # Determine metrics for Body Fat Analysis based on user choice
    if body_fat_choice == 'Percentage (%)':
        selected_metrics_fat = ['Body Fat(%)', '30-day MA Body Fat(%)', '90-day Exponential Smoothing Body Fat(%)']
    else:
        selected_metrics_fat = ['Fat (kg)', '30-day MA Fat (kg)', '90-day Exponential Smoothing Fat (kg)']

    # Main Body Fat Analysis
    st.header('Body Fat Analysis')
    fig_fat = go.Figure()
    for metric in selected_metrics_fat:
        if metric in ['Body Fat(%)', 'Fat (kg)']:
            fig_fat.add_trace(go.Scatter(x=df['Time of Measurement'], y=df[metric], mode='markers', opacity=0.5, name=metric))
        else:
            fig_fat.add_trace(go.Scatter(x=df['Time of Measurement'], y=df[metric], mode='lines', name=metric))
    fig_fat.update_layout(xaxis_title="Date", height=600)
    st.plotly_chart(fig_fat)

    # Sidebar for General Analysis
    st.sidebar.header('Settings for General Analysis')
    general_choice = st.sidebar.radio("Choose metric type for General Analysis", ['All metrics', 'Percentage (%)', 'Kilograms (kg)'])
    
    # Determine metrics for General Analysis based on user choice
    all_metrics = ['Weight(kg)', 'Fat (kg)', 'Body Fat(%)', 'BMI', '30-day MA Weight', '90-day Exponential Smoothing Weight', '30-day MA Body Fat(%)', '90-day Exponential Smoothing Body Fat(%)', '30-day MA Fat (kg)', '90-day Exponential Smoothing Fat (kg)']
    if general_choice == 'Percentage (%)':
        available_metrics = ['Body Fat(%)', '30-day MA Body Fat(%)', '90-day Exponential Smoothing Body Fat(%)']
    elif general_choice == 'Kilograms (kg)':
        available_metrics = ['Weight(kg)', 'Fat (kg)', '30-day MA Weight', '90-day Exponential Smoothing Weight', '30-day MA Fat (kg)', '90-day Exponential Smoothing Fat (kg)']
    else:
        available_metrics = all_metrics

    selected_metrics_general = st.sidebar.multiselect('Select metrics for General Analysis', options=available_metrics, default=['BMI'])

    # Main General Analysis
    st.header('General Analysis')
    fig_general = go.Figure()
    for metric in selected_metrics_general:
        if metric in ['Weight(kg)', 'Fat (kg)', 'Body Fat(%)', 'BMI']:
            fig_general.add_trace(go.Scatter(x=df['Time of Measurement'], y=df[metric], mode='markers', opacity=0.5, name=metric))
        else:
            fig_general.add_trace(go.Scatter(x=df['Time of Measurement'], y=df[metric], mode='lines', name=metric))
    fig_general.update_layout(xaxis_title="Date", height=600)
    st.plotly_chart(fig_general)
    
else:
    st.write("Please upload a CSV file to proceed.")

if __name__ == '__main__':
    pass
