from main import generate_merged_results

# Specify the input file path and output file path
file_path = "MockedData.xlsx"
output_path = "merged_results.csv"

# Call the function and print the result
merged_results_path = generate_merged_results(file_path, merged_results_path=output_path)
print(f"Merged results saved to: {merged_results_path}")
