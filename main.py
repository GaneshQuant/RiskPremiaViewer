import pandas as pd
from backtest_strategy import preprocess_data, backtest_strategy_aligned

# Load the dataset
file_path = "MockedData.xlsx"
data = pd.read_excel(file_path)

# Preprocess the data
data['Maturity'] = pd.to_datetime(data['ExpiryDate'])
data['AsOfDate'] = pd.to_datetime(data['AsOfDate'])
data['T'] = (data['Maturity'] - data['AsOfDate']).dt.days / 365
data_preprocessed = preprocess_data(data)

# Run the backtest
strategy_levels, portfolio_decomposition = backtest_strategy_aligned(data_preprocessed)

# Save the results
strategy_levels_aligned_path = "strategy_levels_aligned.csv"
portfolio_decomposition_aligned_path = "portfolio_decomposition_aligned.csv"
merged_results_path = "merged_results.csv"

unique_dates = data['AsOfDate'].unique()
unique_dates = unique_dates[unique_dates <= pd.Timestamp("2024-06-28")]

# Save strategy levels
results = pd.DataFrame({
    'Date': unique_dates,
    'Strategy Level': strategy_levels
})
results.to_csv(strategy_levels_aligned_path, index=False)

# Save portfolio decomposition
portfolio_df = pd.DataFrame(portfolio_decomposition)
portfolio_df.to_csv(portfolio_decomposition_aligned_path, index=False)

# Merge the CSV files
strategy_df = pd.read_csv(strategy_levels_aligned_path)
portfolio_df = pd.read_csv(portfolio_decomposition_aligned_path)

# Ensure both DataFrames have a consistent date column format
strategy_df['Date'] = pd.to_datetime(strategy_df['Date'])
portfolio_df['date'] = pd.to_datetime(portfolio_df['date'])

# Merge on the date column and rename 'date' to 'Date' before dropping
merged_df = pd.merge(strategy_df, portfolio_df, left_on='Date', right_on='date', how='inner')

# Drop the redundant 'date' column explicitly
if 'date' in merged_df.columns:
    merged_df.drop(columns=['date'], inplace=True)

# Save the merged DataFrame to a CSV file
merged_df.to_csv(merged_results_path, index=False)

print(f"Results saved to {strategy_levels_aligned_path}, {portfolio_decomposition_aligned_path}, and {merged_results_path}")
