import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import json
from datetime import datetime

# Open and read the JSON file
data =None
with open('results.json', 'r') as file:
    data = json.load(file)


# Function for the Forecasting screen
def forecasting():
    st.title('Cash Forecasting')
    # Add forecasting related content here
    import datetime

    # Generate the first day of each month in 2024
    months = ["Jan 24" , 'Feb 24',"Mar 24","Apr 24","May 24","Jun 24","Jul 24","Aug 24","Sep 24","Oct 24","Nov 24","Dec 24"]

    # Create the date range slider
    date_range = st.select_slider(
        "Select forecast range",
        options=months,
        value="Dec 24"
    )



    # Inline buttons for region selection
    # Update session state based on button clicks
    options = ["US", "EUR", "AUD","Consolidated"]
    selection = st.segmented_control(
    "Select Region", options
    )

    # Display the selected region
    if selection:
    # Create two columns for side-by-side graphs
        col1, col2 = st.columns(2)

        # Convert data to DataFrame and process for each metric
        for i, col in zip(['sales', 'inventory'], [col1, col2]):
            with col:
                df = pd.DataFrame(data[selection][i]["historical"])

                # Convert Date column to datetime
                df["Date"] = pd.to_datetime(df["Date"])

                # Create a line plot using Plotly
                fig = px.line(title= i.capitalize()+ " Forecast")

                # Customize the plot for forecast data in 2024
                historical_data = df[df["Date"].dt.year < 2024]
                forecast_data = df[(df["Date"].dt.year >= 2024) & (df["Date"].dt.month <=  datetime.datetime.strptime(date_range, "%b %y").month)]

                fig.add_scatter(
                    x=historical_data["Date"], 
                    y=historical_data["value"], 
                    mode='lines', 
                    name='Historical Data'
                )
                fig.add_scatter(
                    x=forecast_data["Date"], 
                    y=forecast_data["value"], 
                    name='Forecasted Data', 
                    line=dict(dash='dash', color='lightgreen')
                )

                # Display the plot in the respective column
                st.plotly_chart(fig)

        st.write("### Comparison Actual vs Predicted (2024)")
        col1, col2 = st.columns(2)

            # Convert data to DataFrame and process for each metric
        for i, col in zip(['sales', 'inventory'], [col1, col2]):
            with col:
                fig = px.line(title= i.capitalize()+ " Forecast")
                
                df = pd.DataFrame(data[selection][i]["predictions_2024"])
                

                    # Customize the plot for forecast data in 2024

                fig.add_scatter(
                        x=months, 
                        y=df['predicted'], 
                        mode='lines', 
                        name='Predicted',
                        line=dict(dash='dash', color='lightgreen')
                    )
                fig.add_scatter(
                        x=months, 
                        y=df['actual'], 
                        name='Actual',
                        line=dict(color='red')
        
                    )

                    # Display the plot in the respective column
                st.plotly_chart(fig)
                
        variance_bar_graph()

def variance_bar_graph():
    st.write("### Variance of Sales and Inventory Across Regions")

    # Define regions
    regions = ["US", "EUR", "AUD"]

    # Prepare data for sales variance
    sales_data = [{"Region": region, "Variance": data[region]["sales"]["predictions_2024"]["variance"]} for region in regions]
    sales_df = pd.DataFrame(sales_data)

    # Prepare data for inventory variance
    inventory_data = [{"Region": region, "Variance": data[region]["inventory"]["predictions_2024"]["variance"]} for region in regions]
    inventory_df = pd.DataFrame(inventory_data)

    sales_fig = px.bar(
        sales_df,
        x="Region",
        y="Variance",
        color="Region",
        title="Sales Variance Across Regions",
        labels={"Variance": "Variance Value", "Region": "Region"},
        template="plotly_white"
    )
    cols = st.columns(2)
    with cols[0]:
        st.plotly_chart(sales_fig)

    inventory_fig = px.bar(
        inventory_df,
        x="Region",
        y="Variance",
        color="Region",
        title="Inventory Variance Across Regions",
        labels={"Variance": "Variance Value", "Region": "Region"},
        template="plotly_white"
    )
    with cols[1]:
        st.plotly_chart(inventory_fig)
