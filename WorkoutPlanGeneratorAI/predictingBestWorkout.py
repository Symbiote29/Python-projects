import pandas as pd
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression

def create_features(feedback_data):
    features = []
    for _, data in feedback_data.iterrows():
        try:
            user_preferences = eval(data['user_preferences'])
            workout_plan = eval(data['workout_plan'])
            feedback = eval(data['user_feedback'])
        except SyntaxError as e:
            print(f"SyntaxError in row {_}:")
            print(f"user_preferences: {data['user_preferences']}")
            print(f"workout_plan: {data['workout_plan']}")
            print(f"user_feedback: {data['user_feedback']}")
            print("Error message:", e)
            print("-" * 40)

        num_push_exercises = num_pull_exercises = num_legs_exercises = num_abs_exercises = num_cardio_exercises = 0

        if isinstance(workout_plan, list) and isinstance(workout_plan[0], dict):
            for day in workout_plan:
                day_name = day.get('day', '').lower()

                if 'push' in day_name:
                    num_push_exercises += 1
                elif 'pull' in day_name:
                    num_pull_exercises += 1
                elif 'leg' in day_name:
                    num_legs_exercises += 1
                elif 'abs' in day_name:
                    num_abs_exercises += 17
                elif 'cardio' in day_name:
                    num_cardio_exercises += 1
                else:
                    print(f"Uknown day: {day_name}")
        else:
            print("something went wrong")
            print(workout_plan)
            print("Error: workout_plan structure is not as expected")


        goals_muscle_building = 1 if user_preferences['goals'] == 'muscle_building' else 0
        goals_fat_loss = 1 if user_preferences['goals'] == 'fat_loss' else 0
        goals_general = 1 if user_preferences['goals'] == 'general' else 0
        
        cardio = 1 if user_preferences['cardio'] else 0
        
        features.append({
            'days': user_preferences['days'],
            'split': user_preferences['split'],
            'goals_muscle_building': goals_muscle_building,
            'goals_fat_loss': goals_fat_loss,
            'goals_general': goals_general,
            'num_push_exercises': num_push_exercises,
            'num_pull_exercises': num_pull_exercises,
            'num_legs_exercises': num_legs_exercises,
            'num_abs_exercises': num_abs_exercises,
            'num_cardio_exercises': num_cardio_exercises,
            'cardio': cardio,
            'satisfaction': feedback['satisfaction'],
            'progress': feedback['progress'],
            'adherence': feedback['adherence'],
            'effectiveness': feedback['effectiveness']
        })
    
    return pd.DataFrame(features)

df = pd.read_csv('feedbackData_clean.csv', delimiter=';', on_bad_lines='skip', quotechar="'")
df_features = create_features(df)

# https://www.geeksforgeeks.org/python-pandas-get_dummies-method/
# In Pandas, the get_dummies() function converts categorical variables 
# into dummy/indicator variables (known as one-hot encoding). This method
# is especially useful when preparing data for machine learning algorithms that require numeric input.
df_features = pd.get_dummies(df_features, columns=['split'], drop_first=True)

X = df_features.drop(columns=['satisfaction'])
y = df_features['satisfaction']

# random_state=42 bcs 42 is the answer to the great question of “life, the universe and everything”
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

############################# BREAK  ###########################################

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# MSE and R2 prints for testing purposes
print(f"Mean Squared Error (MSE): {mse}")
print(f"R-squared (R2): {r2}")

############################# BREAK  ###########################################

new_user_features = {
    'days': 6,
    'split_push-pull': 2,
    'goals_muscle_building': 1,
    'goals_fat_loss': 0,
    'goals_general': 0,
    'num_push_exercises': 6,
    'num_pull_exercises': 6,
    'num_legs_exercises': 5,
    'num_abs_exercises': 0,
    'cardio': 0
}

def create_new_user_features(new_user_features, X_train_columns):
    goals_muscle_building = 1 if new_user_features['goals_muscle_building'] == 1 else 0
    goals_fat_loss = 1 if new_user_features['goals_fat_loss'] == 1 else 0
    goals_general = 1 if new_user_features['goals_general'] == 1 else 0

    new_user_df = pd.DataFrame([{
        'days': new_user_features['days'],
        'split_push-pull': new_user_features.get('split_push-pull', 0),
        'split_upper-lower': new_user_features.get('split_upper-lower', 0),
        'goals_muscle_building': goals_muscle_building,
        'goals_fat_loss': goals_fat_loss,
        'goals_general': goals_general,
        'num_push_exercises': new_user_features['num_push_exercises'],
        'num_pull_exercises': new_user_features['num_pull_exercises'],
        'num_legs_exercises': new_user_features['num_legs_exercises'],
        'num_abs_exercises': new_user_features['num_abs_exercises'],
        'cardio': new_user_features['cardio'],
        'adherence': 0,
        'effectiveness': 0,
        'progress': 0
    }])

    new_user_df = new_user_df.reindex(columns=X_train_columns, fill_value=0)

    return new_user_df

X_train_columns = X_train.columns

new_user_df = create_new_user_features(new_user_features, X_train_columns)

######################  BREAK ################################

new_user_prediction = model.predict(new_user_df)
new_user_prediction = max(0, min(10, new_user_prediction[0]))

print(f"Predicted Satisfaction for New User: {new_user_prediction}")
