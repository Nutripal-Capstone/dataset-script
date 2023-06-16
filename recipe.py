import aiohttp
import asyncio
import pandas as pd
import os

access_token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjVGQUQ4RTE5MjMwOURFRUJCNzBCMzU5M0E2MDU3OUFEMUM5NjgzNDkiLCJ0eXAiOiJhdCtqd3QiLCJ4NXQiOiJYNjJPR1NNSjN1dTNDeldUcGdWNXJSeVdnMGsifQ.eyJuYmYiOjE2ODQ5NTI0OTksImV4cCI6MTY4NTAzODg5OSwiaXNzIjoiaHR0cHM6Ly9vYXV0aC5mYXRzZWNyZXQuY29tIiwiYXVkIjoicHJlbWllciIsImNsaWVudF9pZCI6Ijk2Y2Y5YzAzZTNlMTRlNmE4YzQ3OGQ1NDdmMjRlNzQzIiwic2NvcGUiOlsicHJlbWllciJdfQ.njJC6vB2dOIye2l7hFCjSB9o9FrK83cx7Vve9L5xlJUBFo6RxJjfnwwL7WPu0xtOXNY9XZ2lY_PFX8a9y9ZF_AFB06aGCFDf7FjMY61b9D0hdUjjCe2BkApODSb727jVmJu8EvhNKlSAf1wm0L4_ntO0o4ryWlPivTU4mQoN-S_7NvDfefIAHlrDN0N8VVuG_kqDPb-LDiay4PLvaW6jXBQFc5oEhZlNeFMWRxqUNxdxeyDr851p30TphbHbz2mO-TMMtCvnMcDmP1krvQB30vYBLRMROM3OVv5PZDlUVLIaVeC8dKiV7a1s8r9IKm_Ck2eSvLiJ-pOFYeXRaJs-7g'
base_url = 'https://platform.fatsecret.com/rest/server.api'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + access_token
}
params = {
    'method': 'recipes.search.v3',
    'format': 'json',
    'max_results': 50,
}

csv_path = 'recipes_only_3.csv'

async def fetch(page_number, session, recipe_item):
    params['search_expression'] = recipe_item
    params['page_number'] = page_number
    async with session.get(base_url, headers=headers, params=params) as response:
        return await response.json()

async def main():
    recipe_items = ['Borscht', 'Mango Sticky Rice', 'Apple', 'Hot Dog', 'Popcorn', 'Yogurt', 'Dumplings', 'Ravioli', 'Pad Thai', 'Lo Mein', 'Spring Roll', 'Carrot Cake', 'Kaya Toast', 'Chimichangas', 'Bread', 'Coconut Oil', 'Berries', 'Nacho', 'Bologna', 'Alfalfa', 'Artichoke', 'Chocolate Chip Cookies', 'Galbi', 'Kebab', 'Beans', 'Olive', 'Celery', 'Cottage Cheese', 'Laksa', 'English Muffin', 'Schnitzel', 'Tortilla Chip', 'Hainanese Chicken Rice', 'Pot Pie', 'Rendang', 'Melt Sandwich', 'Hash Brown', 'Beef', 'Mee Goreng', 'Gazpacho', 'Cornmeal', 'Grape Juice', 'Crab', 'Goulash', 'Flatbread', 'Pickle', 'Strawberry', 'Beet', 'Mussel', 'Pierogi', 'Mushroom', 'Garden Salad', 'Corn Dogs', 'Spinach', 'Lettuce', 'Cheese Pizza', 'Wild Rice', 'Bagel', 'Dried Fruit', 'Green Pea', 'Fried Chicken', 'Blueberry', 'Veggie Burger', 'Chicken Nuggets', 'Veal', 'Cranberry', 'Nutrition Bar', 'Peach', 'Mixed Vegetable', 'Chia Seeds', 'Blackberry', 'Seaweed', 'Gelato', 'Biscuit', 'Stir Fry', 'Cookies', 'Kale', 'Watermelon', 'Fig', 'Jelly', 'Raisin Bran', 'Taco Salad', 'Chip', 'Dakgalbi', 'Smoked Salmon', 'Samosa', 'Bibimbap', 'Calzone', 'Soto Ayam', 'Muffins', 'Chili', 'Zucchini', 'Sardine', 'Smoothie', 'Honey', 'Squash', 'Barley', 'Brussels Sprouts', 'Parsnip', 'Sauerkraut', 'Udon', 'Rice', 'Mousse', 'Snow Pea', 'Rye Bread', 'Turkey', 'Mushrooms', 'Raisin Bread', 'Roasted Potato', 'Brussels Sprout', 'Risotto', 'Fish and Chips', 'Mahi Mahi', 'Fish Tacos', 'Apples', 'Potato', 'Salad', 'Biryani', 'Halibut', 'Pistachios', 'Peking Duck', 'Churros', 'Pilaf', 'Crab Cakes', 'Walnuts', 'Quiche', 'Wrap', 'Tomatoes', 'Jalapeno', 'Taco Shell', 'Roast Chicken', 'Cherry', 'Empanadas', 'Granola', 'Bananas', 'Ramen', 'Bulgur', 'Muesli', 'Cherry Tomato', 'Cabbage Rolls', 'Pretzels', 'Lamb', 'Flounder', 'Doner Kebab', 'Cereal', 'Rice Cake', 'Gado-gado', 'Crawfish', 'Snapper', 'Spaghetti', 'French Fry', 'Garlic', 'Tacos', 'Nectar', 'Salami', 'Tilapia', 'Chocolate Cake', 'Pancakes', 'Brown Rice', 'Roast Pork', 'Japchae', 'Peanut Butter', 'Cannoli', 'Fajitas', 'Oatmeal', 'Fritters', 'Pie Crust', 'Baked Potato', 'Croquette', 'Pecan Pie', 'Egg Rolls', 'Eel', 'Papaya', 'Trail Mix', 'Nutella', 'Rice Noodle', 'Gnocchi', 'Ratatouille', 'Yam', 'Rum', 'Sourdough Bread', 'Maple Syrup', 'Sundubu Jjigae', 'Leek', 'Potato Salad', 'Durian', 'Banh Mi', 'Shallot', 'Shawarma', 'Nectarine', 'Banana', 'Avocado', 'Tempeh', 'Tuna', 'Baby Carrot', 'Oats', 'Wheat Bread', 'Flaxseeds']
    df = pd.read_csv(csv_path) if os.path.isfile(csv_path) else pd.DataFrame()

    async with aiohttp.ClientSession() as session:
        for recipe_item in recipe_items:
            response = await fetch(0, session, recipe_item)
            total_results = int(response.get('recipes', {}).get('total_results', 0))
            print(recipe_item)
            print(total_results)
            num_pages = (total_results // 50) + 1

            tasks = []
            for i in range(num_pages):
                tasks.append(fetch(i, session, recipe_item))

            responses = await asyncio.gather(*tasks)

            rows = []
            for response in responses:
                recipe_results = response.get('recipes', {}).get('recipe', [])
                for recipe in recipe_results:
                    common_data = {key: recipe.get(key, None) for key in ('recipe_id', 'recipe_name', 'recipe_description', 'recipe_image')}
                    common_data['ingredients'] = ', '.join(recipe.get('recipe_ingredients', {}).get('ingredient', []))
                    common_data['recipe_types'] = ', '.join(recipe['recipe_types']['recipe_type']) if 'recipe_types' in recipe and recipe['recipe_types'] is not None else ''
                    
                    nutrition = recipe.get('recipe_nutrition', {})
                    common_data['calories'] = nutrition.get('calories', '')
                    common_data['carbohydrate'] = nutrition.get('carbohydrate', '')
                    common_data['fat'] = nutrition.get('fat', '')
                    common_data['protein'] = nutrition.get('protein', '')

                    rows.append(common_data)

            df = pd.DataFrame(rows)

            if os.path.isfile(csv_path):
                df.to_csv(csv_path, mode='a', header=False, index=False)
            else:
                df.to_csv(csv_path, index=False)

# Run the script
asyncio.run(main())
