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
    return df

st.title('Weight and Health Stats Analysis')

uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    df = load_data(uploaded_file)

    # Sidebar
    st.sidebar.header('Settings')
    selected_metrics = st.sidebar.multiselect(
        'Select metrics to plot', 
        options=['Weight(kg)', 'Fat (kg)', '30-day MA Weight', '90-day Exponential Smoothing Weight', 'BMI', 'Body Fat(%)'],
        default=['Weight(kg)']
    )

    # Main
    if selected_metrics:
        fig = go.Figure()
        for metric in selected_metrics:
            if metric == 'Weight(kg)':
                fig.add_trace(go.Scatter(x=df['Time of Measurement'], y=df[metric], mode='markers', name=metric))
            else:
                fig.add_trace(go.Scatter(x=df['Time of Measurement'], y=df[metric], mode='lines', name=metric))
        fig.update_layout(xaxis_title="Date")
        st.plotly_chart(fig)
    else:
        st.write("Please select at least one metric to display.")
else:
    st.write("Please upload a CSV file to proceed.")

if __name__ == '__main__':
    pass
