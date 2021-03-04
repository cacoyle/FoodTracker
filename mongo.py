from pymongo import MongoClient
import pdb
import datetime

client = MongoClient()

db = client.test_database

meal = {
    "recipe": "Chicken Picatta",
    "date": datetime.datetime.utcnow(),
    "incredients": [
        "chicken",
        "lemon",
        "broccoli",
        "vegetable oil",
        "all purpose flour",
        "garlic",
        "parmessan"
    ]
}

meals = db.meals

meal_id = db.insert_one(meals).inserted_id

pdb.set_Trace()

print("Balls.")
