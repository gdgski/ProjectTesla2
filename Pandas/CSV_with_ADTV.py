import pandas as pd
import numpy as np
import csv

def ADTV_DAYS(dataframe, column, days):
    # Check if the column exists
    # Calculate the moving average
    dataframe[f'ADTV_{days}'] = dataframe[column].rolling(window=days, min_periods=1).mean()

    # Fill the first 4 values of ADTV with the original column value
    dataframe.loc[:4, f'ADTV_{days}'] = dataframe.loc[:4, column]

    # Convert ADTV to integers
    dataframe[f'ADTV_{days}'] = dataframe[f'ADTV_{days}'].astype(int)
    return dataframe

def ADTV_DAYS_std(dataframe, column, days):
        # Calculate the standard deviation of ADTV over a 5-day window
        dataframe[f'ADTV_{days}_std'] = dataframe[column].rolling(window=days, min_periods=1).std()

        # Fill the first 4 values of ADTV_std with 0
        dataframe.loc[:4, f'ADTV_{days}_std'] = dataframe.loc[:4, column]

        # Convert ADTV_std to integers
        dataframe[f'ADTV_{days}_std'] = dataframe[f'ADTV_{days}_std'].astype(int)

        return dataframe

def create_dataframe(file_csv):
# Create a dictionary to then create a dataframe
    with open(f"{file_csv}","r", encoding='utf-8') as f:
        lettore = csv.reader(f, delimiter=',')
        f.readline()
        price_data = []
        for riga in lettore:
            price_data.append(riga)
    # Creation of the dataframe
    dataframe_prices = pd.DataFrame(price_data, columns=["Date","Open","High","Low","Close","Adj Close","Volume"])
    dataframe_prices.replace("", np.nan, inplace=True)
    #changing the type of datas
    dataframe_prices['Date'] = pd.to_datetime(dataframe_prices['Date'])
    dataframe_prices['Open'] = dataframe_prices['Open'].astype(float)
    dataframe_prices['Close'] = dataframe_prices['Close'].astype(float)
    dataframe_prices['Low'] = dataframe_prices['Low'].astype(float)
    dataframe_prices['High'] = dataframe_prices['High'].astype(float)
    dataframe_prices['Adj Close'] = dataframe_prices['Adj Close'].astype(float)
    dataframe_prices['Volume'] = dataframe_prices['Volume'].astype(float)
    df_cleaned = dataframe_prices.dropna().reset_index(drop=True)
    # Salvo il DataFrame 'df_cleaned' su un csv chiamato 'updated_data.csv'
    df_cleaned.to_csv(path_or_buf ="updated_data.csv", index = False)
    return(df_cleaned)


def calculate_mfm(df, high_col="High", low_col="Low", close_col="Close"):
    return ((df[close_col] - df[low_col]) - (df[high_col] - df[close_col])) / (df[high_col] - df[low_col])

final_file = create_dataframe("TSLA_modified.csv")
# Elaborate the ADTV over a period time of 5 days
final_file['ADTV'] = final_file['Volume'].rolling(window=5, min_periods=1).mean()
# fill the first 4 value with the volume of the day itself
final_file['ADTV'].iloc[:4] = final_file['Volume'].iloc[:4]
final_file['ADTV'] = final_file['ADTV'].astype(int)
final_file['ADTV_std'] = final_file['ADTV'].rolling(window=5, min_periods=1).std()
final_file['ADTV_std'].iloc[:4] = 0
final_file['ADTV_std'] = final_file['ADTV_std'].astype(int)
final_file['MFM'] = calculate_mfm(final_file)
final_file["MFV"] = final_file['MFM'] * final_file["Volume"]
final_file["CMF"] = final_file["MFV"].rolling(21).sum() / final_file["Volume"].rolling(21).sum()


df = (final_file[["Date","Volume"]])
result = ADTV_DAYS(final_file, "Volume", 2)
result = ADTV_DAYS_std(result, "Volume", 2)
result = ADTV_DAYS(final_file, "Volume", 5)
result = ADTV_DAYS_std(result, "Volume", 5)
result = ADTV_DAYS(final_file, "Volume", 10)
result = ADTV_DAYS_std(result, "Volume", 10)
result = ADTV_DAYS(final_file, "Volume", 20)
result = ADTV_DAYS_std(result, "Volume", 20)
result = ADTV_DAYS(final_file, "Volume", 50)
result = ADTV_DAYS_std(result, "Volume", 50)
result_finale = (final_file[["Date","Open","High","Low","Close","Adj Close","Volume","ADTV_2","ADTV_2_std","ADTV_5","ADTV_5_std","ADTV_10","ADTV_10_std","ADTV_20","ADTV_20_std","ADTV_50","ADTV_50_std", "MFM", "CMF"]])

# Save the DataFrame in a CSV file
result_finale.to_csv('ADTV_TSLA.csv', index=False)

def to_json(file_csv):
    with open(f'{file_csv}', 'r', encoding='utf-8') as f:
        lettore = list(csv.reader(f, delimiter=','))
        chiavi = lettore[0]
        json_da_esportare = []
        for riga in lettore[1:]:
            dizionario = {}
            for i in range(len(chiavi)):
                chiave = chiavi[i]
                valore = riga[i]
                dizionario[chiave] = valore
            json_da_esportare.append(dizionario)
            return json_da_esportare
