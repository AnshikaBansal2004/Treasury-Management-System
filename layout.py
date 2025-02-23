import streamlit as st
from current_dashboard import curr_dashboard
from cash_forecast import forecasting
from summary_report import summary
from ai_forecast import decision
from upload import upload

# Main function to control the layout and navigation
def main():
    

    # Create a placeholder to manage the state of the selected tab
    if "selected_tab" not in st.session_state:
        st.session_state.selected_tab = "Home"  # Default tab
    # Define the sidebar buttons
    st.sidebar.title("Welcome to TREZO! ")
    st.sidebar.write("")
    if st.sidebar.button("Home", use_container_width=True):
        st.session_state.selected_tab = "Home"
    if st.sidebar.button("Cash Forecasting", use_container_width=True):
        st.session_state.selected_tab = "Cash Forecasting"
    if st.sidebar.button("Summary Report", use_container_width=True):
        st.session_state.selected_tab = "Summarized Report"
    if st.sidebar.button("Prognosis", use_container_width=True):
        st.session_state.selected_tab = "AI Forecast"
    if st.sidebar.button("Upload Statements", use_container_width=True):
        st.session_state.selected_tab = "Upload Statements"
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.clear()  # Clears session state
        st.rerun()  # Reruns the app to reset it

    # Render content based on the selected tab
    if st.session_state.selected_tab == "Home":
        curr_dashboard()  # Call the `curr_dashboard()` function

    elif st.session_state.selected_tab == "Cash Forecasting":
        forecasting()  # Call the `forecasting()` function

    elif st.session_state.selected_tab == "Summarized Report":
        summary()  # Call the `summary()` function

    elif st.session_state.selected_tab == "AI Forecast":
        decision()  # Call the `decision()` function
    elif st.session_state.selected_tab == "Upload Statements":
        upload()  # Call the `upload()` function
    
