import pymongo
client = pymongo.MongoClient("mongodb+srv://gregoriodegiuli2:generation123@clustertsla.mmjht.mongodb.net/")
mydb = client["DB_TSLA"]
collezione = mydb["CL_TSLA"]
from CSV_cleaning import json_da_esportare
risultato = collezione.insert_many(json_da_esportare)



