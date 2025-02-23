import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dateutil.relativedelta import relativedelta 
import base64

# Function for the Dashboard screen
def curr_dashboard(): 


    # Function to preprocess the visible dataset
    def preprocess_visible_data(data):
        # Extract the year from the 'date' column
        year_column = pd.to_datetime(data['Date'], format='%b-%y').dt.year
        # Filter out rows where the year is 2024
        data = data[year_column != 2024]
        return data

    # Load the visible dataset
    df_visible = pd.read_csv('dataset.csv')
    df_visible = preprocess_visible_data(df_visible)

    # Function to load and preprocess the Excel data
    def load_data(file_path, sheet_name):
        data = pd.read_excel(file_path, sheet_name=sheet_name, index_col=0)  # Load data from specified sheet
        data = data.T  # Transpose to make months the index and factors the columns
        # Convert month labels to datetime format
        data.index = pd.to_datetime(data.index, format="%b-%y")
        return data

    # Function to clean the data (remove commas and convert to numeric)
    def clean_data(data):
        for col in data.columns:
            data[col] = data[col].replace({',': ''}, regex=True)  
            data[col] = pd.to_numeric(data[col], errors='coerce')  
        return data

    # File path and sheet names
    file_path = "liquidity.xlsx"
    sheet_names = {
        "US": "US Entity",
        "EUR": "EUR Entity",
        "AUS": "AUD Entity",
    }

    # Factors for each region
    factors_dict = {
        "US": [
            "Loan Receipt", "Loan Payment", "Stock Issue/Repurchase", 
            "Purchase/Sale of Plant, property, equipment", "Purchase/Sale of marketable securities",
            "Mergers And Acquisitions", "Sales Receipts", "Accounts Receivable", 
            "Other Income", "Intercompany Receipts", "Accounts Payable", 
            "Purchase of Inventory", "Payroll", "Promotion and marketing", 
            "Tax", "Insurance", "Bank Fees", "Legal Fees", "Rent"
        ],
        "EUR": [
            "Loan Receipt", "Loan Payment", "Stock Issue/Repurchase", 
            "Purchase/Sale of Plant, property, equipment", "Purchase/Sale of marketable securities", 
            "Mergers And Acquisitions", "Accounts Receivable", "Sales Receipts", 
            "Accounts Payable", "Purchase of Inventory", "Payroll", "Payroll Taxes", 
            "Tax", "Insurance", "Bank Fees", "Legal Fees", "Rent"
        ],
        "AUS": [
            "Loan Receipt", "Loan Payment", 
            "Purchase/Sale of Plant, property, equipment", "Purchase/Sale of marketable securities",
            "Accounts Receivable", "Sales Receipts", "Intercompany Receipts", 
            "Accounts Payable", "Purchase of Inventory", "Payroll", "Payroll Taxes", 
            "Tax", "Insurance", "Bank Fees", "Legal Fees", "Rent"
        ]
    }


    # Header and Title
    st.title("Treasury Management System")

    # Button state for showing/hiding data
    if "show_data" not in st.session_state:
        st.session_state.show_data = False

    if st.button("View Table" if not st.session_state.show_data else "Hide Table"):
        st.session_state.show_data = not st.session_state.show_data
        st.rerun()

    # Display table based on the button state
    if st.session_state.show_data:
        st.markdown("Consolidated Data Table For All Entities")
        st.dataframe(df_visible)
    
    view_option = st.selectbox("Select View:", ["Consolidated", "Regional"])
    

    # Main page layout for term selection and view selection
    col1, col2, col3, col4, col5 = st.columns([2, 1, 3, 1, 3])

    with col1:
        if(view_option!="Consolidated"):
            year_selection = st.segmented_control("Year:", [2022, 2023],default=2022)

    with col3:
        if(view_option!="Consolidated"):
            months = st.slider(
            "Select Term Duration:",
            min_value=1,
            max_value=12,
            value=6,
            step=1,
            format="%d months",
        )

    with col5:
        if(view_option!="Consolidated"):
            region = st.selectbox("Select Region:", ['US', 'EUR', 'AUS'])
            # st.markdown(f"### Regional View - {region}")
        

    if view_option == "Consolidated":
        st.markdown("### Consolidated View")
        st.markdown(
                """<a href="https://app.powerbi.com/groups/me/reports/5f82a75c-ea44-443d-8564-5f6b96ffb21a/012c4b580d9a9e4970dc?experience=power-bi">
                <img src="data:image/png;base64,{}" width="100%">
                </a>""".format(
                    base64.b64encode(open("powerbi.png", "rb").read()).decode()
                ),
                unsafe_allow_html=True,
            )
        # st.markdown("""<iframe title="ANSHIKA DASHBOARD" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=00b7ea36-39a5-496e-8bab-7dfa30c28ae5&autoAuth=true&ctid=768fe7d4-ebee-41a7-9851-d5825ecdd396" frameborder="0" allowFullScreen="true"></iframe>""",unsafe_allow_html=True)
    
    # elif view_option == "Regional":
    #     region = st.selectbox("Select Region:", ['US', 'EUR', 'AUS'])
    #     st.markdown(f"### Regional View - {region}")

    elif view_option == "Compare":
        regions_to_compare = st.multiselect(
            "Select Regions to Compare:", ['US', 'EUR', 'AUS']
        )
        if regions_to_compare:
            st.markdown("### Comparison View")
   
    if view_option == "Regional":
        st.markdown(f"### Regional View - {region}")
        available_factors = factors_dict.get(region, [])
        factors = st.multiselect(
            "Select Features", 
            available_factors, 
            help="Select one or more features to visualize."
        )
        # st.markdown(
        #     f"<h1 style='font-size: 40px; text-align: center;'>{region} Dashboard</h1>",
        #     unsafe_allow_html=True
        # )
        # st.subheader("Tracking of Financial Factors") 
        sheet_name = sheet_names.get(region, "US Entity")
        data = load_data(file_path, sheet_name)
        data = clean_data(data)

        currency = {"US": "USD (Dollars)", "EUR": "EUR (Euros)", "AUS": "AUD (Australian Dollars)"}.get(region, "")
        
        start_date = pd.to_datetime(f"Jan {year_selection or 2022}", format="%b %Y")
        
        end_date = start_date + relativedelta(months=months)
        

        filtered_data = data[(data.index >= start_date) & (data.index <= end_date)]

        if factors:
            fig = go.Figure()
            colors = px.colors.qualitative.Set2

            for idx, factor in enumerate(factors):
                if factor in filtered_data.columns:
                    fig.add_trace(go.Scatter(
                        x=filtered_data.index, 
                        y=filtered_data[factor], 
                        mode='lines+markers',
                        name=factor,
                        line=dict(color=colors[idx % len(colors)]),
                        marker=dict(size=10, symbol='circle', line=dict(width=2, color='black')),
                        hovertemplate="%{text}<br>Value: %{y}<br>Date: %{x}<extra></extra>",
                        text=filtered_data[factor].round(2)
                    ))
                else:
                    st.error(f"Feature '{factor}' not found in the data.")

            fig.update_layout(
                title=f"{region} - Factor Graph ({currency})",
                xaxis_title="Date",
                yaxis_title=f"Value ({currency})",
                template="plotly_dark",
                height=600,
                width=1000,
                margin={"t": 50, "b": 50, "l": 50, "r": 50},
                xaxis=dict(
                    tickformat='%b %y',
                    tickmode='array',
                    tickvals=filtered_data.index[::3],
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(255, 255, 255, 0.2)'
                ),
                plot_bgcolor='rgba(0, 0, 0, 0.1)',
                hoverlabel=dict(
                    bgcolor='black',
                    font_size=14,
                    font_color='white'
                ),
            )
            st.plotly_chart(fig)
        else:
            st.warning("Please select at least one feature to display the graph.")

