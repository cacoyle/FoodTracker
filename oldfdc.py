import requests

import config as c

def grams_to_ounces(grams, round_up=True):
    from math import ceil

    ounces = grams / 28.34952

    if round_up:
        return ceil(ounces)

    return ounces

meal = {
    'boneless skinless chicken breast': 8,
    'broccoli florets': 8
}

ingredients = {
    'chicken breast': {
        'value': 8,
        'unit': 'oz'
    }
}

ingredient_ids = []

for i,v in meal.items():
    print(i)

    # Need to play with filters, see if I can get a legit 'generic'
    # brand id
    result = requests.post(
        'https://api.nal.usda.gov/fdc/v1/foods/search',
        params={
            'api_key': c.USDA_API_KEY
        },
        json={
            # 'query': 'boneless skinless chicken breast',
            'query': i,
            'dataType': [
                'Branded',
            ],
            # 'pageSize': 1,
            # 'brandOwner': 'Perdue Farms Incorporated'
        }
    )

    ingredient_ids.append(result.json()['foods'][0]['fdcId'])

ingredient_details = requests.get(
    'https://api.nal.usda.gov/fdc/v1/foods',
    params={
        'api_key': c.USDA_API_KEY,
        'fdcIds': ','.join([str(x) for x in ingredient_ids]),
        'nutrients': 1008  # Calories
    }
)

breakpoint()

for i in ingredient_details.json():
    if i['servingSizeUnit'] == 'g':
        portion_size = grams_to_ounces(i['servingSize'])

        cals_per_portion = i['labelNutrients']['calories']['value']

        total_calories = (ingredient_amount / portion_size) * cals_per_portion

        print(f'Chicken Breast - {ingredient_amount}oz: {total_calories} calories')

print("Balls.")
