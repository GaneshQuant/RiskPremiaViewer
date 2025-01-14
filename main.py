import pandas as pd
from backtest_strategy import preprocess_data, backtest_strategy_aligned

def generate_merged_results(file_path, merged_results_path="merged_results.csv"):
    # Load the dataset
    data = pd.read_excel(file_path)

    # Preprocess the data
    data['Maturity'] = pd.to_datetime(data['ExpiryDate'])
    data['AsOfDate'] = pd.to_datetime(data['AsOfDate'])
    data['T'] = (data['Maturity'] - data['AsOfDate']).dt.days / 365
    data_preprocessed = preprocess_data(data)

    # Run the backtest
    strategy_levels, portfolio_decomposition = backtest_strategy_aligned(data_preprocessed)

    # Create strategy levels DataFrame
    unique_dates = data['AsOfDate'].unique()
    unique_dates = unique_dates[unique_dates <= pd.Timestamp("2024-06-28")]
    strategy_df = pd.DataFrame({
        'Date': unique_dates,
        'Strategy Level': strategy_levels
    })

    # Create portfolio decomposition DataFrame
    portfolio_df = pd.DataFrame(portfolio_decomposition)

    # Ensure date column consistency
    strategy_df['Date'] = pd.to_datetime(strategy_df['Date'])
    portfolio_df['date'] = pd.to_datetime(portfolio_df['date'])

    # Merge on the date column and clean up redundant columns
    merged_df = pd.merge(strategy_df, portfolio_df, left_on='Date', right_on='date', how='inner')
    merged_df.drop(columns=['date'], inplace=True)

    # Save the merged results
    merged_df.to_csv(merged_results_path, index=False)
    return merged_results_path
