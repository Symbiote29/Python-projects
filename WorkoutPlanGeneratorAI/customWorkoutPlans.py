import pandas as pd
import random

df = pd.read_csv("all_exercises_per_category.csv", sep=";")

exercises_dict = {}
categorized_exercises = {'push': [], 'pull': [], 'legs': [], 'cardio': [], 'abs': []}

for index, row in df.iterrows():
    exercise_name = row['Name']
    primary_muscle = row['Primary Muscle'].split(", ") if isinstance(row['Primary Muscle'], str) else []
    secondary_muscle = row['Secondary Muscle'].split(", ") if isinstance(row['Secondary Muscle'], str) else []
    
    if not primary_muscle and not secondary_muscle:
        muscles_targeted = row['Category']
    else:
        muscles_targeted = primary_muscle + secondary_muscle
    
    exercises_dict[exercise_name] = {
        "category": row['Category'],
        "muscles_targeted": muscles_targeted,
        "equipment": row['Equipment'] if 'Equipment' in row else "varied",
        "difficulty": row['Difficulty'] if 'Difficulty' in row else "unknown",
        "exercise_type": row['Type'] if 'Type' in row else "compound",
        "goal": row['Goal'] if 'Goal' in row else "general",
    }

def categorize_exercises(exercises_dict):
    for exercise, data in exercises_dict.items():
        muscles_targeted = [muscle.strip().lower() for muscle in data['muscles_targeted']]
        category = data['category'].lower().strip()
        
        if any(muscle in ['chest', 'shoulders', 'triceps'] for muscle in muscles_targeted) or 'shoulders' in category:
            categorized_exercises['push'].append(exercise)
        
        elif any(muscle in ['back', 'lats', 'biceps'] for muscle in muscles_targeted) or 'back' in category:
            categorized_exercises['pull'].append(exercise)
        
        elif any(muscle in ['legs', 'quads', 'hamstrings', 'calves'] for muscle in muscles_targeted) or 'legs' in category:
            categorized_exercises['legs'].append(exercise)
        
        elif 'cardio' in category:
            categorized_exercises['cardio'].append(exercise)

        elif 'abs' in category:
            categorized_exercises['abs'].append(exercise)

categorize_exercises(exercises_dict)

def get_user_preferences():
    user_preferences = {}
    
    user_preferences['days'] = random.choice([3, 4, 5, 6])  # Randomly generate days (3-6)
    user_preferences['split'] = random.choice(['push-pull', 'upper-lower', 'full-body'])  # Random split
    user_preferences['goals'] = random.choice(['muscle_building', 'fat_loss', 'general'])  # Random goal
    user_preferences['cardio'] = random.choice([True, False])  # Randomly decide if user wants cardio
    
    user_preferences['muscles'] = random.sample(['push', 'pull', 'legs', 'abs'], random.randint(1, 4))
    
    return user_preferences

def generate_workout_plan(user_preferences):
    workout_plan = []
    
    push_exercises = categorized_exercises['push']
    pull_exercises = categorized_exercises['pull']
    legs_exercises = categorized_exercises['legs']
    abs_exercises = categorized_exercises['abs']
    cardio_exercises = categorized_exercises['cardio']
    
    if 'push' in user_preferences['muscles'] and len(push_exercises) >= 6:
        for day in range(user_preferences['days']//2):
            workout_plan.append({
                'day': f'Push Day {day + 1}',
                'exercises': random.sample(push_exercises, 6)
            })
    
    if 'pull' in user_preferences['muscles'] and len(pull_exercises) >= 6:
        for day in range(user_preferences['days']//2):
            workout_plan.append({
                'day': f'Pull Day {day + 1}',
                'exercises': random.sample(pull_exercises, 6)
            })

    if 'legs' in user_preferences['muscles'] and len(legs_exercises) >= 6:
        workout_plan.append({
            'day': 'Leg Day',
            'exercises': random.sample(legs_exercises, 6)
        })

    if 'abs' in user_preferences['muscles'] and len(abs_exercises) >= 6:
        workout_plan.append({
            'day': 'Abs Day',
            'exercises': random.sample(abs_exercises, 6)
        })
    
    if user_preferences['cardio'] and len(cardio_exercises) > 6:
        workout_plan.append({
            'day': 'Cardio Day',
            'exercises': random.sample(cardio_exercises, 6)
        })
    return workout_plan

def generateUserFeedback(user_preferences):
    userFeedback = {}
    x = y = z = 0
    deduction = random.randrange(0,2)
    surplus = random.randrange(0,2)
    
    userFeedback['satisfaction'] = (lambda: random.randrange(7,10) if user_preferences['days'] > 4 else random.randrange(1,6))()
    x = (lambda: random.randrange(7,10) if user_preferences['days'] > 4 else random.randrange(1,6))()
    y = (lambda: random.randrange(7,10) if user_preferences['days'] > 4 else random.randrange(1,6))()
    z = (lambda: random.randrange(7,10) if user_preferences['days'] > 3 else random.randrange(1,6))()

    userFeedback['progress'] = (lambda: x - deduction if user_preferences['cardio'] else x)()
    userFeedback['adherence'] = (lambda: y - deduction if user_preferences['cardio'] == True else y)()
    userFeedback['effectiveness'] = (lambda: z + surplus if user_preferences['cardio'] == True else z)()

    return userFeedback

workout_plans_data = []

for _ in range(500):
    user_preferences = get_user_preferences()
    workout_plan = generate_workout_plan(user_preferences)
    user_feedback = generateUserFeedback(user_preferences)
    
    workout_plans_data.append({
        'user_preferences': user_preferences,
        'workout_plan': workout_plan,
        'user_feedback': user_feedback
    })


df = pd.DataFrame(workout_plans_data)

df.to_csv("feedbackData.csv", index=False, encoding='utf-8', sep=';')


# for plan in workout_plans_data:
#     feedback_storage.add_feedback_entry(plan['user_preferences'], plan['workout_plan'], plan['user_feedback'])
# print(feedback_storage.get_feedback_data())
