import json
from pymongo import MongoClient
from bson import ObjectId

def convert_oid(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict) and "$oid" in value:
                data[key] = ObjectId(value["$oid"])
            else:
                data[key] = convert_oid(value)
    elif isinstance(data, list):
        return [convert_oid(item) for item in data]
    return data

with open('100docs.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

json_data = convert_oid(json_data)

client = MongoClient('mongodb://localhost:27017/')
db = client['docs']  
collection = db['collection']  

if isinstance(json_data, list):
    collection.insert_many(json_data)
else:
    collection.insert_one(json_data)

print("Data inserted successfully!")
