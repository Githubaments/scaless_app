import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    # Ensure the first column's name is 'Time of Measurement'
    df.rename(columns={df.columns[0]: 'Time of Measurement'}, inplace=True)
    # Convert the 'Time of Measurement' column to datetime
    df['Time of Measurement'] = pd.to_datetime(df['Time of Measurement'])
    df['Fat (kg)'] = (df['Body Fat(%)'] / 100) * df['Weight(kg)']
    df['30-day MA Weight'] = df['Weight(kg)'].rolling(window=30).mean()
    df['90-day Exponential Smoothing Weight'] = df['Weight(kg)'].ewm(span=90).mean()
    df['30-day MA Body Fat(%)'] = df['Body Fat(%)'].rolling(window=30).mean()
    df['90-day Exponential Smoothing Body Fat(%)'] = df['Body Fat(%)'].ewm(span=90).mean()
    df['30-day MA Fat (kg)'] = df['Fat (kg)'].rolling(window=30).mean()
    df['90-day Exponential Smoothing Fat (kg)'] = df['Fat (kg)'].ewm(span=90).mean()
    return df

# Generate moving averages dynamically for each metric
def generate_ma_refactored(df, metrics):
    new_columns = {}
    for metric in metrics:
        new_columns[f'30-day MA {metric}'] = df[metric].rolling(window=30).mean()
        new_columns[f'90-day Exponential Smoothing {metric}'] = df[metric].ewm(span=90).mean()
    
    # Joining all new columns to the original DataFrame
    for col_name, col_data in new_columns.items():
        df[col_name] = col_data
    
    return df
def calculate_fat_loss(current_weight, current_bf_percentage, target_bf_percentage):
    body_fat_mass = current_weight * (current_bf_percentage / 100)
    lbm = current_weight - body_fat_mass
    goal_weight = lbm / (1 - target_bf_percentage / 100)
    weight_to_lose = current_weight - goal_weight
    return weight_to_lose

def calculate_fat_volume(weight_to_lose):
    # Assuming density of body fat is approximately 900 kg/m^3
    return weight_to_lose / 900

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

    ma_mappings_extended = {
    'Weight(kg)': ['30-day MA Weight', '90-day Exponential Smoothing Weight'],
    'Fat (kg)': ['30-day MA Fat (kg)', '90-day Exponential Smoothing Fat (kg)'],
    'Body Fat(%)': ['30-day MA Body Fat(%)', '90-day Exponential Smoothing Body Fat(%)']
}


    st.sidebar.header('Settings for General Analysis')
    raw_metrics = ['Weight(kg)', 'Fat (kg)', 'BMI', 'Body Fat(%)', 'Fat-free Body Weight(kg)', 
                   'Subcutaneous Fat(%)', 'Visceral Fat', 'Body Water(%)', 'Skeletal Muscle(%)', 
                   'Muscle Mass(kg)', 'Bone Mass(kg)', 'Protein(%)', 'BMR(kcal)', 'Metabolic Age']
    selected_metrics_general = st.sidebar.multiselect('Select metrics for General Analysis', options=raw_metrics, default=['BMI'])

    # Generate moving averages for the selected metrics and add them to the list of metrics to plot
    mas = []
    for metric in selected_metrics_general:
        ma_30 = f'30-day MA {metric}'
        ma_90 = f'90-day Exponential Smoothing {metric}'
        
        df[ma_30] = df[metric].rolling(window=30).mean()
        df[ma_90] = df[metric].ewm(span=90).mean()
        
        mas.extend([ma_30, ma_90])
    
    selected_metrics_general += mas

    # Main General Analysis
    st.header('General Analysis')
    fig_general = go.Figure()
    for metric in selected_metrics_general:
        if metric in raw_metrics:
            fig_general.add_trace(go.Scatter(x=df['Time of Measurement'], y=df[metric], mode='markers', opacity=0.5, name=metric))
        else:
            fig_general.add_trace(go.Scatter(x=df['Time of Measurement'], y=df[metric], mode='lines', name=metric))
    fig_general.update_layout(xaxis_title="Date", height=600)
    st.plotly_chart(fig_general)





    st.title('Body Fat Loss Calculator')

    # Extract the last values
    current_weight = df['Weight(kg)'].iloc[-1]
    current_bf_percentage = df['Body Fat(%)'].iloc[-1]

    st.write(f"Using last recorded weight: **{current_weight}kg** with body fat of **{current_bf_percentage}%**.")
    # Calculate the difference in 'Fat (kg)'
    current_fat = df['Fat (kg)'].iloc[-1]  # Assuming the latest value is at the end of the DataFrame
    # First, sort the DataFrame by 'Fat (kg)' in descending order to get the highest value
    df_sorted = df.sort_values(by='Fat (kg)', ascending=False)

    # Get the highest 'Fat (kg)' value
    highest_fat = df_sorted.iloc[0]['Fat (kg)']

    fat_difference = current_fat - highest_fat
    
    # Display the difference in 'Fat (kg)'
    st.write(f"Difference in **Fat (kg)** between now and peak: **{-fat_difference:.2f} kg**.")
    
    volume_lost = calculate_fat_volume(fat_difference)
    
    st.write(f"This equates to a volume of approximately **{-volume_lost*1000:.1f} liters**.")

    # User input for target
    target_bf_percentage = st.slider("Enter your target body fat percentage:", min_value=1, max_value=50, value=15, step=1)

    # Calculate and display result
    if st.button('Calculate'):

        fat_to_lose = calculate_fat_loss(current_weight, current_bf_percentage, target_bf_percentage)
        st.write(f"To reach a body fat percentage of {target_bf_percentage}%, you need to lose approximately **{fat_to_lose:.2f} kg**.")

        volume_to_lose = calculate_fat_volume(fat_to_lose)
        st.write(f"This equates to a volume of approximately **{volume_to_lose*1000:.1f} liters**.")

    
else:
    st.write("Please upload a CSV file to proceed.")

if __name__ == '__main__':
    pass
