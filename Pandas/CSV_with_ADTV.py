from CSV_cleaning import create_dataframe
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
final_file = create_dataframe("TSLA_modified.csv")
# Elaborate the ADTV over a period time of 5 days
final_file['ADTV'] = final_file['Volume'].rolling(window=5, min_periods=1).mean()
# fill the first 4 value with the volume of the day itself
final_file['ADTV'].iloc[:4] = final_file['Volume'].iloc[:4]
final_file['ADTV'] = final_file['ADTV'].astype(int)
final_file['ADTV_std'] = final_file['ADTV'].rolling(window=5, min_periods=1).std()
final_file['ADTV_std'].iloc[:4] = 0
final_file['ADTV_std'] = final_file['ADTV_std'].astype(int)
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
result_finale = (final_file[["Date","Open","High","Low","Close","Adj Close","Volume","ADTV_2","ADTV_2_std","ADTV_5","ADTV_5_std","ADTV_10","ADTV_10_std","ADTV_20","ADTV_20_std","ADTV_50","ADTV_50_std"]])
print(result_finale)
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
