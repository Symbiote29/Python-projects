import requests
import pandas as pd

response_categories = requests.get('https://wger.de/api/v2/exercisecategory/')
categories = response_categories.json()

exercise_list = []

def fetch_data(url, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

muscle_base_url = "https://wger.de/api/v2/muscle/"
equipment_base_url = "https://wger.de/api/v2/equipment/"

for category in categories['results']:
    category_id = category['id']
    category_name = category['name']
    
    print(f"Fetching exercises for category: {category_name} (ID: {category_id})...")
    next_page = f"https://wger.de/api/v2/exercise/?language=2&category={category_id}"
    
    while next_page:
        data = fetch_data(next_page, {"category": category_id})

        if 'results' in data:
            for exercise in data['results']:
                primary_muscle_ids = exercise['muscles']
                secondary_muscle_ids = exercise['muscles_secondary']
                equipment_ids = exercise['equipment']

                primary_muscles = [fetch_data(f"{muscle_base_url}{muscle_id}/")['name_en'] for muscle_id in primary_muscle_ids]
                secondary_muscles = [fetch_data(f"{muscle_base_url}{muscle_id}/")['name_en'] for muscle_id in secondary_muscle_ids]
                equipment_names = [fetch_data(f"{equipment_base_url}{eq_id}/")['name'] for eq_id in equipment_ids]
    
                exercise_list.append({
                    "ID": exercise['id'],
                    "Name": exercise['name'],
                    "Category": category_name,
                    "Primary Muscle": ", ".join(primary_muscles),
                    "Secondary Muscle": ", ".join(secondary_muscles),
                    "Equipment": ", ".join(equipment_names)
                })
        
        next_page = data.get("next")

df = pd.DataFrame(exercise_list)

df.to_csv("all_exercises_per_category.csv", index=False, encoding='utf-8', sep=';')

#print(df) 
