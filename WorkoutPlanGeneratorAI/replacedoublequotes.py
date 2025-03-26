import pandas as pd

df = pd.read_csv("feedbackData.csv", sep=";")

df = df.applymap(lambda x: str(x).replace('"', "'") if isinstance(x, str) else x)

df.to_csv("feedbackData_clean.csv", sep=";", index=False)

