import csv
from CSV_cleaning import create_dataframe

df_mfm = create_dataframe("TSLA_modified.csv")
print(df_mfm)

def calculate_mfm(df, high_col="High", low_col="Low", close_col="Close"):

    return ((df[close_col] - df[low_col]) - (df[high_col] - df[close_col])) / (df[high_col] - df[low_col])

# Example usage
df_mfm["MFM"] = calculate_mfm(df_mfm)
result = (df_mfm[["Date", "MFM"]])
