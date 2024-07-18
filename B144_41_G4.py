import pandas as pd


def calculate_numerical_means(df):
    """Calculate the mean of each numerical column in the DataFrame.

    Args:
    df (pd.DataFrame): The input DataFrame.

    Returns:
    pd.Series: A Series containing the mean of each numerical column.
    """
    numerical_means = df.select_dtypes(include='number').mean()
    return numerical_means


def count_unique_categorical_values(df):
    """Count the number of unique values in each categorical column.

    Args:
    df (pd.DataFrame): The input DataFrame.

    Returns:
    pd.Series: A Series containing the unique value counts for each categorical column.
    """
    unique_counts = df.select_dtypes(include='object').nunique()
    return unique_counts


def calculate_missing_value_percentages(df):
    """Calculate the percentage of missing values for each column.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.Series: A Series containing the percentage of missing values for each column.
    """
    # Calculate missing value percentages by column
    missing_percentages = df.isnull().sum() * 100 / len(df)
    return missing_percentages


# Load the CSV file
file_path = '/workspaces/clean_code/sample_csv.csv'
df = pd.read_csv(file_path)

# Calculate means
numerical_means = calculate_numerical_means(df)
print("Means of numerical columns:\n", numerical_means)

# Count unique values
unique_counts = count_unique_categorical_values(df)
print("Unique value counts in categorical columns:\n", unique_counts)

# Calculate missing value percentages and print them
missing_percentages = calculate_missing_value_percentages(df)
print("Missing value percentages:\n", missing_percentages)
