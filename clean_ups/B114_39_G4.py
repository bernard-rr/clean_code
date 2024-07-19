import pandas as pd


# Specify the path to your CSV file
file_path = '/workspaces/clean_code/sample_csv.csv' 

# Load the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Explore the DataFrame
print(df.head()) # View the first few rows 
print(df.info()) # Get summary information about the DataFrame

# Further processing or analysis can be done with the DataFrame
