import csv
from CSV_cleaning import create_dataframe

df_mfm = create_dataframe("TSLA_modified.csv")
print(df_mfm)

def calculate_mfm(df, high_col="High", low_col="Low", close_col="Close"):
    """
    Calculate the Market Facilitation Index (MFM).

    Parameters:
        df (pd.DataFrame): The DataFrame containing market data.
        high_col (str): Column name for high prices.
        low_col (str): Column name for low prices.
        close_col (str): Column name for close prices.

    Returns:
        pd.Series: A Pandas Series containing the MFM values.
    """
    return ((df[close_col] - df[low_col]) - (df[high_col] - df[close_col])) / (df[high_col] - df[low_col])

# Example usage
df_mfm["MFM"] = calculate_mfm(df_mfm)
result = (df_mfm[["Date", "MFM"]])
print(result)
result.to_csv('MFM.csv', index=False)