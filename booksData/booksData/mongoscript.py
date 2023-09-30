from pymongo import MongoClient
client = MongoClient("mongodb+srv://anushkanaik47:Anushka2525@newproject.ztjulpt.mongodb.net/")
db = client.test_database
collection = db.test_collection
import datetime
post = {
    "author": "Mike",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.now(tz=datetime.timezone.utc),
}

post_id = collection.insert_one(post).inserted_id