from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import mysql.connector
from mysql.connector import Error

app = FastAPI()

# Cargar el modelo y el scaler
model = joblib.load('random_forest.joblib')
scaler = joblib.load('scaler.joblib')

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
        connection = mysql.connector.connect(
            host='localhost:3306',
            database='diabetes_predictions',
            user='your_username',
            password='your_password'
        )
        
        cursor = connection.cursor()
        query = """INSERT INTO predictions 
                   (HighBP, HighChol, CholCheck, BMI, Smoker, Stroke, HeartDiseaseorAttack,
                    PhysActivity, Fruits, Veggies, HvyAlcoholConsump, AnyHealthcare,
                    NoDocbcCost, GenHlth, MentHlth, PhysHlth, DiffWalk, Sex, Age,
                    Education, Income, prediction) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                           %s, %s, %s, %s, %s, %s, %s)"""
        values = (features.HighBP, features.HighChol, features.CholCheck, features.BMI,
                  features.Smoker, features.Stroke, features.HeartDiseaseorAttack,
                  features.PhysActivity, features.Fruits, features.Veggies,
                  features.HvyAlcoholConsump, features.AnyHealthcare, features.NoDocbcCost,
                  features.GenHlth, features.MentHlth, features.PhysHlth, features.DiffWalk,
                  features.Sex, features.Age, features.Education, features.Income, prediction)
        cursor.execute(query, values)
        connection.commit()
    except Error as e:
        print(f"Error al guardar en la base de datos: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()