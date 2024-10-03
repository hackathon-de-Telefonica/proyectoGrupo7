from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np
import sqlite3
import os

app = FastAPI()

# Cargar el modelo y el scaler
with open('random_forest_model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

# Asegurarse de que la base de datos existe
db_path = 'diabetes_predictions.db'
if not os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE predictions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  HighBP INTEGER, HighChol INTEGER, CholCheck INTEGER, BMI REAL,
                  Smoker INTEGER, Stroke INTEGER, HeartDiseaseorAttack INTEGER,
                  PhysActivity INTEGER, Fruits INTEGER, Veggies INTEGER,
                  HvyAlcoholConsump INTEGER, AnyHealthcare INTEGER, NoDocbcCost INTEGER,
                  GenHlth INTEGER, MentHlth INTEGER, PhysHlth INTEGER, DiffWalk INTEGER,
                  Sex INTEGER, Age INTEGER, Education INTEGER, Income INTEGER,
                  prediction REAL, prediction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

class DiabetesFeatures(BaseModel):
    HighBP: int
    HighChol: int
    CholCheck: int
    BMI: float
    Smoker: int
    Stroke: int
    HeartDiseaseorAttack: int
    PhysActivity: int
    Fruits: int
    Veggies: int
    HvyAlcoholConsump: int
    AnyHealthcare: int
    NoDocbcCost: int
    GenHlth: int
    MentHlth: int
    PhysHlth: int
    DiffWalk: int
    Sex: int
    Age: int
    Education: int
    Income: int

@app.post("/predict")
async def predict_diabetes(features: DiabetesFeatures):
    try:
        feature_array = np.array([[
            features.HighBP, features.HighChol, features.CholCheck, features.BMI,
            features.Smoker, features.Stroke, features.HeartDiseaseorAttack,
            features.PhysActivity, features.Fruits, features.Veggies,
            features.HvyAlcoholConsump, features.AnyHealthcare, features.NoDocbcCost,
            features.GenHlth, features.MentHlth, features.PhysHlth, features.DiffWalk,
            features.Sex, features.Age, features.Education, features.Income
        ]])
        
        scaled_features = scaler.transform(feature_array)
        prediction = model.predict_proba(scaled_features)[0][1]
        
        save_to_database(features, prediction)
        
        return {"probability": float(prediction)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def save_to_database(features: DiabetesFeatures, prediction: float):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = """INSERT INTO predictions 
                   (HighBP, HighChol, CholCheck, BMI, Smoker, Stroke, HeartDiseaseorAttack,
                    PhysActivity, Fruits, Veggies, HvyAlcoholConsump, AnyHealthcare,
                    NoDocbcCost, GenHlth, MentHlth, PhysHlth, DiffWalk, Sex, Age,
                    Education, Income, prediction) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        values = (features.HighBP, features.HighChol, features.CholCheck, features.BMI,
                  features.Smoker, features.Stroke, features.HeartDiseaseorAttack,
                  features.PhysActivity, features.Fruits, features.Veggies,
                  features.HvyAlcoholConsump, features.AnyHealthcare, features.NoDocbcCost,
                  features.GenHlth, features.MentHlth, features.PhysHlth, features.DiffWalk,
                  features.Sex, features.Age, features.Education, features.Income, prediction)
        cursor.execute(query, values)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error al guardar en la base de datos: {e}")
    finally:
        if conn:
            conn.close()