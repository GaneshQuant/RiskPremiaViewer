import streamlit as st
import pandas as pd
from pandas import Timestamp

# Load the merged dataset
@st.cache_data
def load_data():
    merged_results_path = "merged_results.csv"
    
    # Load the merged dataset
    merged_data = pd.read_csv(merged_results_path)
    
    # Convert the Date column to datetime
    merged_data['Date'] = pd.to_datetime(merged_data['Date'])
    
    return merged_data

# Load the data
try:
    merged_data = load_data()
except FileNotFoundError:
    st.error("The merged_results.csv file is missing. Please ensure it is in the app directory.")
    st.stop()

# Streamlit App
st.title("Options Strategy Viewer")

# Ensure data is loaded before continuing
if 'merged_data' in locals() and not merged_data.empty:
    # Date input
    selected_date = st.date_input(
        "Select a date to view the strategy details:",
        value=merged_data['Date'].min(),
        min_value=merged_data['Date'].min(),
        max_value=merged_data['Date'].max()
    )

    # Filter data based on the selected date
    data_for_date = merged_data[merged_data['Date'] == pd.Timestamp(selected_date)]

    if not data_for_date.empty:
        # Display Strategy Level
        strategy_level = data_for_date.iloc[0]['Strategy Level']
        st.subheader(f"Strategy Level: {strategy_level:.2f}")

        # Extract call and put positions
        call_positions = data_for_date['call_positions'].iloc[0]
        put_positions = data_for_date['put_positions'].iloc[0]

        try:
            call_positions_df = pd.DataFrame(eval(call_positions))
            put_positions_df = pd.DataFrame(eval(put_positions))
        except Exception as e:
            st.error(f"Error processing option positions: {e}")
            st.stop()

        # Select columns to display
        columns_to_display = ['strike', 'delta', 'maturity', 'units']

        st.subheader("Call Options")
        st.table(call_positions_df[columns_to_display])

        st.subheader("Put Options")
        st.table(put_positions_df[columns_to_display])

        # Fetch and display underlying delta properly
        if 'underlying_delta' in data_for_date.columns:
            underlying_delta = data_for_date['underlying_delta'].iloc[0]
            st.subheader(f"Underlying Delta: {underlying_delta:.5f}")
        else:
            st.error("Underlying Delta field is missing from the dataset.")
    else:
        st.warning("No data available for the selected date.")
else:
    st.warning("Data is not loaded. Please ensure the required CSV files are in the directory.")
