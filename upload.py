import streamlit as st
import pandas as pd



# Function for the Forecasting screen
def upload():
    st.title('Upload Bank Records')
    df_backend = pd.read_csv('dataset.csv')

    # Single uploader for multiple files
    uploaded_files = st.file_uploader("Upload up to 3 CSV files", type=["csv"], accept_multiple_files=True)

    # Placeholder for viewing uploaded data
    

    # Store data visibility state
    if "show_data" not in st.session_state:
        st.session_state.show_data = False
        st.rerun()
    view_data=None
    if uploaded_files:
        if  not st.session_state.show_data:
            view_data = st.button("View Data")
        else:
            view_data = st.button("Hide Data")
    

    if view_data:
        st.session_state.show_data = not st.session_state.show_data
        st.rerun()

    # Process uploaded files
    if uploaded_files:
        files_uploaded = 0
        for i, file in enumerate(uploaded_files):
            try:
                # Read CSV file
                df = pd.read_csv(file)
                if st.session_state.show_data:
                    st.markdown(f"#### Table : {file.name.strip(".csv").strip(".pdf").strip(".xlsx")} Entity ")
                    st.dataframe(df)
                files_uploaded += 1
            except Exception as e:
                st.error(f"Error reading file {i+1}: {e}")

        # Display df_backend after all three files are uploaded
        if files_uploaded == 3:
            st.markdown("### Consolidated Data Table")
            st.dataframe(df_backend)
    else:
        st.info("Please upload CSV files to get started.")