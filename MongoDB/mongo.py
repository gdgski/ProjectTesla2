import pymongo
import csv
def to_json(file_csv):
    with open(f'{file_csv}','r', encoding='utf-8') as f:
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

list_of_dicts = to_json("ADTV_TSLA.csv")


client = pymongo.MongoClient("mongodb+srv://gregoriodegiuli2:generation123@clustertsla.mmjht.mongodb.net/")
mydb = client["DB_TSLA"]
collezione = mydb["CL_TSLA"]
risultato = collezione.insert_many(list_of_dicts)



