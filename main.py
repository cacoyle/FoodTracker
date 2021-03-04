from pydantic import BaseModel
from pymongo import MongoClient
from typing import List, Optional
from fastapi import FastAPI

from pdb import set_trace as breakpoint

import arrow
import config
import json

class Ingredient(BaseModel):
    name: str
    unit: str
    size: int

class Recipe(BaseModel):
    title: str
    date: int
    category: str
    ingredients: List[Ingredient] = []
    total_calories: int

client = MongoClient()

mongo_db = client.test_recipes

test_recipe = {
    'title': 'lemon chicken broccoli pasta',
    'date': int(arrow.utcnow().timestamp()),
    'category': 'main',
    'ingredients': [
        {
            'name': 'chicken breast',
            'unit': 'oz',
            'size': 8
        },
        {
            'name': 'broccoli',
            'unit': 'oz',
            'size': 8
        },
        {
            'name': 'pasta',
            'unit': 'oz',
            'size': 6
        }
    ],
    'total_calories': 800
}

meal = Recipe(**test_recipe)


app = FastAPI()

@app.get('/recipes')
def read_root():
    result = mongo_db.recipes.find_one()

    result.pop('_id')

    return result

@app.post('/recipes/new')
def new_recipe(recipe: Recipe):
    breakpoint()
    new_recipe = mongo_db.recipes
    result = new_recipe.insert_one(json.loads(recipe.json()))
    return recipe
