from MoneyFlowMultiplier import calculate_mfm
from MoneyFlowMultiplier import df_mfm
from MoneyFlowMultiplier import result

df_mfm["MFV"] = calculate_mfm(df_mfm) * df_mfm["Volume"]
df_mfm["CMF"] = df_mfm["MFV"].rolling(21).sum() / df_mfm["Volume"].rolling(21).sum()

resultfinale = (df_mfm[["Date", "MFM", "CMF"]])

resultfinale.to_csv('CMF.csv', index=False)


