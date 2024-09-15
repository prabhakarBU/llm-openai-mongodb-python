import pandas as pd
import json
from pymongo import MongoClient
# from pymongo.server_api import ServerApi

try:
    uri = "mongodb+srv://username:password@database-url.mongodb.net/?retryWrites=true&w=majority&appName=app"
    # Create a new client and connect to the server
    client = MongoClient(uri)
    print('Connected to MongoDB server successfully.')

    db = client['amazon-product-reviews']
    collection = db['reviews']
    print('Selected database and collection successfully.')

    # collection.drop()
    
    data = pd.read_csv("amazon-product-reviews/Reviews.csv").head(500)
    print(len(data))
    print('read the data')
    # result = collection.insert_many(data)
    #1st way
    document = data.to_dict('records')
    print('converted to document')
    # print(document)
    # result = collection.insert_many(document)
    # print('Document inserted:', result.inserted_id)


except Exception as e:
    print("exception" , e)
