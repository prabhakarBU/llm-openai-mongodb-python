from pymongo import MongoClient

try:
    uri = "mongodb+srv://username:password@database-url.mongodb.net/?retryWrites=true&w=majority&appName=app"
    # Create a new client and connect to the server
    client = MongoClient(uri)
    print('Connected to MongoDB server successfully.')

    db = client['amazon-product-reviews']
    collection = db['reviews']
    print('Selected database and collection successfully.')
    
    collection.create_index([('ProfileName','text'),('Summary','text'),('Text','text')])
    print('Index created on the collection successfully.')
    
except Exception as e:
    print("exception" , e)
