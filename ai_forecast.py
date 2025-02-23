import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Input and output directories
input_directory = './'  # Update to your folder path
output_directory = './'
os.makedirs(output_directory, exist_ok=True)

# Function to load predictions from a JSON file
def load_predictions(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Function to process predictions
def process_predictions(predictions_data, region, parameter, adjustment_percentage, start_month):
    if region not in predictions_data:
        raise ValueError(f"Region {region} not found in predictions data")

    region_data = predictions_data[region]
    if parameter not in region_data:
        raise ValueError(f"Parameter {parameter} not found for region {region}")

    predictions = region_data[parameter]["predictions_2024"]["predicted"]
    variance = region_data[parameter]["predictions_2024"]["variance"]

    # Convert predictions to DataFrame
    months = pd.date_range(start='2024-01-01', periods=12, freq='M')
    df = pd.DataFrame({
        'date': months,
        'value': predictions
    })

    # Apply adjustment
    start_date = pd.to_datetime(start_month, format='%m-%Y')
    df['adjusted_value'] = df['value'].copy()
    df.loc[df['date'] >= start_date, 'adjusted_value'] *= (1 + adjustment_percentage / 100)

    return df, variance

# Function to plot adjustments
def plot_adjustments(df, region, parameter):
    fig = make_subplots()

    # Add the original predictions line
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['value'],
        mode='lines+markers',
        name='Forecasted Predictions',
        marker=dict(symbol='circle')
    ))

    # Add the adjusted predictions line
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['adjusted_value'],
        mode='lines+markers',
        name='Adjusted Predictions',
        marker=dict(symbol='x')
    ))

    # Update the layout
    fig.update_layout(
        title=f"{region} {parameter.capitalize()} Predictions 2024",
        xaxis_title="Date",
        yaxis_title=parameter.capitalize(),
        legend_title="Legend",
        xaxis=dict(tickangle=45),
        template="plotly_white"
    )

    return fig
def decision():
    # Main Streamlit interface
    st.title("Prognosis Dashboard")
    st.write("##### Aims to forecast financial impacts based on user-provided business scenarios")

    # Input text box for user prompt
    # Default scenario
    default_scenario = "New US factory set up in January 2024, with sales expected to rise by 12% and inventory purchases to drop by 5%"

    # Text input field that updates with session state
    user_prompt = st.text_input("Enter Scenarios",placeholder=default_scenario)
    if user_prompt:
        import time
        with st.spinner(f"Generating..."):
            time.sleep(2)
        # Simulate AI response parsing
        ai_response = {
            "sales": 12,  # Example adjustment percentage
            "inventory": -5,
            "month": "01-2024",
            "region": "US"
        }

        try:
            # Load predictions data
            predictions_file = os.path.join(input_directory, "results.json")
            predictions_data = load_predictions(predictions_file)

            # Process predictions for each parameter
            for parameter, adjustment in ai_response.items():
                if parameter in ["sales", "inventory"]:
                    df, variance = process_predictions(
                        predictions_data,
                        ai_response["region"],
                        parameter,
                        adjustment,
                        ai_response["month"]
                    )

                    # Plot the adjustments
                    fig = plot_adjustments(df, ai_response["region"], parameter)
                    st.plotly_chart(fig)

                    # Show impact summary
                    original_total = df['value'].sum()
                    adjusted_total = df['adjusted_value'].sum()
                    net_change = adjusted_total - original_total

                    st.write(f"### Results for {parameter.capitalize()}")
                    st.write(f"- **Original Total**: {original_total}")
                    st.write(f"- **Adjusted Total**: {adjusted_total}")
                    st.write(f"- **Net Change**: {net_change}")
                    st.write(f"- **Percentage Change**: {adjustment}%")
                    st.write(f"- **Variance**: {variance}")

        except Exception as e:
            st.error(f"Error: {str(e)}")
