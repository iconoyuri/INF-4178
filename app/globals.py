import os
from dotenv import load_dotenv
load_dotenv()

APP_NAME = os.getenv("APP_NAME")

DB_USERNAME = os.getenv("DB_USERNAME")
DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@cluster0.jdrid1t.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))[DB_NAME]
# print(client['collection'].find())

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

encodeing='utf8'

FRONTEND_DOMAIN = os.getenv("FRONTEND_DOMAIN")

