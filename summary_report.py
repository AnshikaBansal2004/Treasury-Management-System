import streamlit as st
import time
import pandas as pd
import numpy as np

# Function for the Summary screen


def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)


def summary():
    st.title("Summary Report")
    st.write("##### AI-generated reports for your periodic cash flow history and region")

    # Select Date Range using a slider
    import datetime

    # Define the start and end dates
    start_date = datetime.date(2022, 1, 1)
    end_date = datetime.date(2024, 12, 31)

    # Create the date range slider
    date_range = st.slider(
        "Select date range",
        min_value=start_date,
        max_value=end_date,
        value=(start_date, datetime.date(2022, 12, 1)),
        format="MMM YY",
        step=datetime.timedelta(days=30),  
    )


    # Inline buttons for region selection
    # Update session state based on button clicks
    options = ["USA", "Europe", "Australia", "Consolidated"]
    selection = st.segmented_control(
    "Select Region", options
    )

    # Display the selected region
    if selection:
        col1,col2,col3 = st.columns(3)
        # Add a button to generate the summary
        with col1 :
            generate = st.button("Generate Summary")
            # Placeholder for report generation logic
        start_date_str = date_range[0].strftime("%b %y")            
        end_date_str = date_range[1].strftime("%b %y")

        # Use the formatted dates in the spinner message
        
            
        if generate:
            with st.spinner(f"Generating report for {selection} region from {start_date_str} to {end_date_str}..."):
                time.sleep(2)
                with col3:
                    st.download_button("Download Report", "", "Report")
                text = """**Summary Report: Analysis of Financial Data (Jan-22 to Dec-22)**

This report summarizes the trends observed in the provided financial data from January 2022 to December 2022.  The data includes various income and expense categories, providing a comprehensive overview of the company's financial activities during this period.  All currency values are in US Dollars.

**Summary of Data:**

The dataset encompasses twelve months of financial records, detailing key financial activities such as sales receipts, loan receipts and payments, stock transactions, capital expenditure (Plant, property, equipment), investment activities (marketable securities), operating expenses (payroll, inventory purchases, etc.), and other income streams.

**Significant Trends and Anomalies:**

Several notable trends and anomalies were observed within the provided data:

1. **Sales Receipts:**  Sales receipts show a significant increase from January to June, peaking at $6,048,000,000 in June.  Following this peak, sales show a sharp decrease, although there is a slight increase again in October. This represents a substantial fluctuation that requires further investigation.

2. **Purchase of Inventory:**  There's a marked increase in purchase of inventory from January to September.  The cost of inventory purchase rises steadily and significantly until September, and then decreases slightly in the following months. This substantial rise requires deeper analysis to understand the underlying reasons. The exceptionally large increase from February to March ($168,480,000 to $702,000,000) is a noteworthy anomaly.

3. **Accounts Payable:** Accounts payable exhibit a generally increasing trend throughout the year. The increase is particularly pronounced in November,  experiencing a dramatic jump to -$654,080,918. This spike is a significant outlier compared to the previous months and requires careful examination.

4. **Payroll:**  Payroll expenses show a steady increase throughout the year, with a dramatic jump in November. The increase from October to November ($98,861,351.62 to $193,071,122.04) is highly notable and warrants detailed investigation into the cause.

5. **Other Income:**  "Other Income" shows substantial fluctuations throughout the year. It is worth investigating the sources and consistency behind this variability to better understand the factors affecting this income stream. The value of "Other Income" is comparatively low in March and August.

6. **Purchase/Sale of Plant, Property, and Equipment:** This category shows a consistent increase in capital expenditures throughout the year, indicating significant investment in fixed assets.


7. **Loan Activities:** While loan receipts show some variability, loan payments show a general decreasing trend, though with some fluctuations.

8. **Stock Issue/Repurchase:** This activity is minimal throughout most of the year, with notable spikes only occurring in February and December,  suggesting infrequent strategic financial decisions related to equity.


**Conclusion:**

The analysis reveals several significant fluctuations and trends in the company's financial performance during the period.  The identified spikes and dips in sales, inventory purchases, accounts payable, and payroll are particularly noteworthy and require further investigation to identify the underlying causes and implications.  The large increase in capital expenditure requires further contextual analysis as well.

"""
                
            
            st.write_stream(stream_data(text))
