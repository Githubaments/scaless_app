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
    selected_metrics_fat = st.sidebar.multiselect(
        'Select metrics for Body Fat Analysis', 
        options=['Body Fat(%)', 'Fat (kg)', '30-day MA Body Fat(%)', '90-day Exponential Smoothing Body Fat(%)', '30-day MA Fat (kg)', '90-day Exponential Smoothing Fat (kg)'],
        default=['Body Fat(%)', '30-day MA Body Fat(%)', '90-day Exponential Smoothing Body Fat(%)']
    )

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
    
else:
    st.write("Please upload a CSV file to proceed.")

if __name__ == '__main__':
    pass



