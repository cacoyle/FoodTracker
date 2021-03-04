from math import ceil

import requests

import config as c

def grams_to_ounces(grams, round_up=True):

    ounces = grams / 28.34952

    if round_up:
        return ceil(ounces)

    return ounces

def ml_to_oz(ml, round_up=True):
    # 15ml = 1 tbsp / .5oz

    oz = ml / 30

    if round_up:
        return ceil(oz)

    return oz


meal = {
    'boneless skinless chicken breast': {
        'brand': None,
        'unit': 'oz',
        'value': 8,
        'fdcId': None
    },
    'broccoli florets': {
        'brand': None,
        'unit': 'oz',
        'value': 8,
        'fdcId': None
    },
    'olive oil': {
        'brand': None,
        'unit': 'tbsp',
        'value': 1,
        'fdcId': None
    },
    'fusilli': {
        'brand': None,
        'unit': 'oz',
        'value': 8,
        'fdcId': None
    }
}

ingredient_ids = []

for i in meal:
    print(i)
    result = requests.post(
        'https://api.nal.usda.gov/fdc/v1/foods/search',
        params={
            'api_key': c.USDA_API_KEY
        },
        json={
            'query': i,
            'dataType': [
                'Branded',
            ],
            # 'pageSize': 1,
            # 'brandOwner': 'Perdue Farms Incorporated'
        }
    )

    meal[i].update({'fdcId': result.json()['foods'][0]['fdcId']})



ingredient_details = requests.get(
    'https://api.nal.usda.gov/fdc/v1/foods',
    params={
        'api_key': c.USDA_API_KEY,
        'fdcIds':  ','.join([str(meal[x]['fdcId']) for x in meal]),
        'nutrients': 1008  # Calories
    }
)

total_cals = 0

volume_ids = {meal[x]['fdcId']: meal[x]['value'] for x in meal}

for i in ingredient_details.json():
    if i['servingSizeUnit'] == 'g':
        portion_size = grams_to_ounces(i['servingSize'])

    if i['servingSizeUnit'] == 'ml':
        portion_size = ml_to_oz(i['servingSize'])

    cals_per_portion = i['labelNutrients']['calories']['value']

    total_calories = ceil((volume_ids[i['fdcId']] / portion_size) * cals_per_portion)

    total_cals += total_calories

    print(f'{i["description"]} - {volume_ids[i["fdcId"]]}oz: {total_calories} calories')

print(f'Total calories: {total_cals}')
