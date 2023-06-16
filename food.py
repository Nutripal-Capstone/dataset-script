import aiohttp
import asyncio
import pandas as pd
import os

access_token = ''''''
base_url = 'https://platform.fatsecret.com/rest/server.api'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + access_token
}
params = {
    'method': 'foods.search.v2',
    'format': 'json',
    'max_results': 50,
    'flag_default_serving': "true"
}

csv_path = 'food_brand_only_S.csv'

async def fetch(page_number, session, food_item):
    params['search_expression'] = food_item
    params['page_number'] = page_number
    async with session.get(base_url, headers=headers, params=params) as response:
        return await response.json()

async def main():
    food_items = ["Bagel", "Biscuit", "Bread", "Breadstick", "Bun", "Cereal", "Cornbread", "Croissant", "English Muffin", "Flatbread", "Focaccia", "Garlic Bread", "Granola", "Muesli", "Multigrain Bread", "Naan", "Oatmeal", "Oats", "Pita Bread", "Potato Bread", "Raisin Bread", "Roll", "Rye Bread", "Scone", "Sourdough Bread", "Toast", "Tortilla", "Wheat Bread", "White Bread", "Whole Wheat Bread", "Wrap",  "Anchovy", "Calamari", "Carp", "Catfish", "Clam", "Cod", "Crab", "Crawfish", "Eel", "Fish", "Flounder", "Haddock", "Halibut", "Herring", "Lobster", "Mackerel", "Mahi Mahi", "Mussel", "Octopus", "Oyster", "Salmon", "Sardine", "Scallop", "Shrimp", "Smoked Salmon", "Snapper", "Squid", "Swordfish", "Tilapia", "Trout", "Tuna",  "Brown Rice", "Couscous", "Fried Rice", "Gnocchi", "Jambalaya", "Lasagna", "Macaroni", "Macaroni and Cheese", "Noodle", "Paella", "Pasta", "Pilaf", "Polenta", "Ravioli", "Rice", "Risotto", "Spaghetti", "Tortellini", "White Rice", "Wild Rice",  "Apple", "Apricot", "Avocado", "Banana", "Berry", "Blackberry", "Blueberry", "Cantaloupe", "Cherry", "Coconut", "Cranberry", "Date", "Dried Fruit", "Fig", "Fruit Salad", "Grapefruit", "Grape", "Honeydew Melon", "Kiwifruit", "Litchi", "Mandarin Orange", "Mango", "Melon", "Nectarine", "Orange", "Papaya", "Peach", "Pear", "Pineapple", "Plum", "Prune", "Raisin", "Raspberry", "Strawberry", "Watermelon",  "Burger", "Burrito", "Calzone", "Cheese Pizza", "Cheeseburger", "Chicken Nugget", "Curry", "Enchilada", "Fajita", "French Fry", "Hamburger", "Hash Brown", "Hot Dog", "Nacho", "Onion Ring", "Pepperoni Pizza", "Pizza", "Quesadilla", "Taco", "Tostada", "Veggie Burger",  "Cereal Bar", "Breakfast Bar", "Chip", "Corn Chip", "Cracker", "Crispbread", "Granola Bar", "Gum", "Jerky", "Nutrition Bar", "Popcorn", "Potato Chip", "Pretzel", "Rice Cake", "Sandwich", "Sushi", "Tortilla Chip", "Trail Mix",  "Alfalfa", "Almond Butter", "Almond Milk", "Apple Pie", "Barley", "Bison", "Blueberry Pie", "Bulgur", "Capers", "Carrot Cake", "Casseroles", "Challah", "Cherry Pie", "Chilaquiles", "Chimichangas", "Chocolate Cake", "Chocolate Chip Cookies", "Chow Mein", "Cobbler", "Collards", "Corn Dogs", "Cornmeal", "Croutons", "Desserts", "Dumplings", "Egg Rolls", "Eggnog", "Empanadas", "Falafel", "French Toast", "Fritters", "Fruit Cocktail", "Gelatin",  "Goulash", "Grape Juice", "Grapefruit Juice", "Grits", "Gyro", "Hominy", "Horseradish", "Lo Mein", "Melt Sandwich", "Mousse", "Nectar", "Nougat", "Nutrition Drink", "Pate", "Pecan Pie", "Pie Crust", "Pot Pie", "Potato Skin", "Protein Powder", "Quiche", "Raisin Bran", "Red Potato", "Rice Noodle", "Roasted Potato", "Rum", "Samosa", "Sandwich Cookie", "Sauerkraut", "Seaweed", "Shallot", "Sherbet", "Snow Pea", "Soy Yogurt", "Spread", "Spring Roll", "Stir Fry", "Sun-Dried Tomato", "Supplement", "Tabouli", "Taco Shell", "Tamale", "Taquito", "Tempeh", "Tempura", "Topping", "Water Chestnut",  "Artichoke", "Asparagus", "Baby Carrot", "Baked Potato", "Beet", "Broccoli", "Brussels Sprout", "Cabbage", "Carrot", "Cauliflower", "Celery", "Cherry Tomato", "Corn", "Corn on the Cob", "Cucumber", "Edamame", "Eggplant", "Garlic", "Green Pea", "Jalapeno", "Kale", "Leek", "Lettuce", "Mashed Potato", "Mixed Vegetable", "Mushroom", "Okra", "Olive", "Onion", "Parsnip", "Pea", "Pepper", "Pickle", "Potato", "Pumpkin", "Radish", "Spinach", "Squash", "Succotash", "Sweet Potato", "Tomato", "Turnip", "Yam", "Zucchini",  "Caesar Salad", "Chicken Salad", "Coleslaw", "Egg Salad", "Garden Salad", "Greek Salad", "Pasta Salad", "Potato Salad", "Salad", "Taco Salad", "Tuna Salad"]


    df = pd.read_csv(csv_path) if os.path.isfile(csv_path) else pd.DataFrame()

    async with aiohttp.ClientSession() as session:
        for food_item in food_items:
            response = await fetch(0, session, food_item)
            total_results = int(response.get('foods_search', {}).get('total_results', 0))
            print(total_results)
            num_pages = (total_results // 50) + 1

            tasks = []
            for i in range(num_pages):
                tasks.append(fetch(i, session, food_item))

            responses = await asyncio.gather(*tasks)

            rows = []
            for response in responses:
                food_search = response.get('foods_search')
                if food_search is not None:
                    results = food_search.get('results', {})
                    if results:  # Only proceed if 'results' is not an empty dict
                        food_results = results.get('food', [])
                        for food in food_results:
                            if food.get('food_type') == "Brand":
                                try:
                                    common_data = {**{key: food.get(key, None) for key in ('food_id', 'food_name', 'food_type', 'food_url', 'brand_name')}}
                                    servings = food.get('servings', {}).get('serving', [])
                                    for serving in servings:
                                        if serving.get('is_default', '0') == '1':
                                            # Define all possible keys and default values
                                            serving_data = {
                                                'serving_id': None, 'serving_description': None, 'serving_url': None,
                                                'metric_serving_amount': None, 'metric_serving_unit': None,
                                                'number_of_units': None, 'measurement_description': None,
                                                'calories': None, 'carbohydrate': None, 'protein': None,
                                                'fat': None, 'saturated_fat': None, 'polyunsaturated_fat': None,
                                                'monounsaturated_fat': None, 'trans_fat': None,
                                                'cholesterol': None, 'sodium': None, 'potassium': None,
                                                'fiber': None, 'sugar': None, 'added_sugars': None,
                                                'vitamin_d': None, 'vitamin_a': None, 'vitamin_c': None,
                                                'calcium': None, 'iron': None
                                            }
                                            # Update the keys that exist in the serving
                                            serving_data.update({key: serving.get(key, None) for key in serving_data.keys()})
                                            # Add common data and serving data into row
                                            row = {**common_data, **serving_data}
                                            rows.append(row)
                                            break
                                except Exception as e:
                                    print(f"An error occurred: {e}")
                                    continue

            df = pd.DataFrame(rows)

            if os.path.isfile(csv_path):
                df.to_csv(csv_path, mode='a', header=False, index=False)
            else:
                df.to_csv(csv_path, index=False)

# Run the script
asyncio.run(main())

