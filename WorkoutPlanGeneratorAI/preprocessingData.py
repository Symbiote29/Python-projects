import requests
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

df = pd.read_csv("all_exercises_per_category.csv", sep=";")

# Convert string-based muscle lists to actual lists
df["Primary Muscle"] = df["Primary Muscle"].apply(lambda x: x.split(", ") if isinstance(x, str) else [])
df["Secondary Muscle"] = df["Secondary Muscle"].apply(lambda x: x.split(", ") if isinstance(x, str) else [])

# Combine primary and secondary muscles into a single column
df["Muscle Targets"] = df["Primary Muscle"] + df["Secondary Muscle"]

# Multi-label binarizer (MLB) to convert muscle names into one-hot encoding
# one-hot encoding -> used for converting categorical values into binary
# 1 -> category is present
# 2 -> category is not present

mlb = MultiLabelBinarizer()
y = mlb.fit_transform(df["Muscle Targets"])

# TF-IDF vectorizer to convert exercise names into numerical features
# (Term Frequency-Inverse Document Frequency) is a statistical measure 
# used in natural language processing and information retrieval to evaluate 
# the importance of a word in a document relative to a collection of documents

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["Name"])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=mlb.classes_))
