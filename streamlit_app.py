import joblib
import numpy as np
import streamlit as st
import requests
import pandas as pd
import mysql.connector
from mysql.connector import Error

st.title('Predicción de Diabetes')

# Formulario de entrada
HighBP = st.selectbox('Presión arterial alta', [0, 1])
HighChol = st.selectbox('Colesterol alto', [0, 1])
CholCheck = st.selectbox('Chequeo de colesterol', [0, 1])
BMI = st.number_input('IMC', min_value=0.0, max_value=50.0, value=25.0)
Smoker = st.selectbox('Fumador', [0, 1])
Stroke = st.selectbox('Accidente cerebrovascular', [0, 1])
HeartDiseaseorAttack = st.selectbox('Enfermedad cardíaca o ataque', [0, 1])
PhysActivity = st.selectbox('Actividad física', [0, 1])
Fruits = st.selectbox('Consumo de frutas', [0, 1])
Veggies = st.selectbox('Consumo de verduras', [0, 1])
HvyAlcoholConsump = st.selectbox('Consumo excesivo de alcohol', [0, 1])
AnyHealthcare = st.selectbox('Tiene seguro de salud', [0, 1])
NoDocbcCost = st.selectbox('No visita al médico por costo', [0, 1])
GenHlth = st.slider('Salud general', min_value=1, max_value=5, value=3)
MentHlth = st.slider('Días de mala salud mental en el último mes', min_value=0, max_value=30, value=0)
PhysHlth = st.slider('Días de mala salud física en el último mes', min_value=0, max_value=30, value=0)
DiffWalk = st.selectbox('Dificultad para caminar', [0, 1])
Sex = st.selectbox('Sexo', [0, 1])
Age = st.slider('Edad', min_value=18, max_value=100, value=30)
Education = st.slider('Nivel de educación', min_value=1, max_value=6, value=4)
Income = st.slider('Nivel de ingresos', min_value=1, max_value=8, value=4)

if st.button('Predecir'):
    # Preparar los datos para la API
    data = {
        "HighBP": HighBP,
        "HighChol": HighChol,
        "CholCheck": CholCheck,
        "BMI": BMI,
        "Smoker": Smoker,
        "Stroke": Stroke,
        "HeartDiseaseorAttack": HeartDiseaseorAttack,
        "PhysActivity": PhysActivity,
        "Fruits": Fruits,
        "Veggies": Veggies,
        "HvyAlcoholConsump": HvyAlcoholConsump,
        "AnyHealthcare": AnyHealthcare,
        "NoDocbcCost": NoDocbcCost,
        "GenHlth": GenHlth,
        "MentHlth": MentHlth,
        "PhysHlth": PhysHlth,
        "DiffWalk": DiffWalk,
        "Sex": Sex,
        "Age": Age,
        "Education": Education,
        "Income": Income
    }
    
    # Hacer la solicitud a la API
    response = requests.post("http://localhost:8000/predict", json=data)
    
    if response.status_code == 200:
        result = response.json()
        probability = result["probability"]
        st.write(f"La probabilidad de tener diabetes es: {probability:.2%}")
    else:
        st.error("Hubo un error al hacer la predicción.")

# Mostrar predicciones anteriores
st.subheader("Predicciones Anteriores")

try:
    connection = mysql.connector.connect(
        host='localhost',
        database='diabetes_predictions',
        user='your_username',
        password='your_password'
    )
    
    query = "SELECT * FROM predictions ORDER BY id DESC LIMIT 10"
    df = pd.read_sql(query, connection)
    st.dataframe(df)
except Error as e:
    st.error(f"Error al conectar con la base de datos: {e}")
finally:
    if connection.is_connected():
        connection.close()
import matplotlib.pyplot as plt

def plot_feature_importance(model, feature_names):
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    plt.figure(figsize=(10,6))
    plt.title("Importancia de Características")
    plt.bar(range(len(importances)), importances[indices])
    plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=90)
    plt.tight_layout()
    st.pyplot(plt)

# Cargar el modelo
model = joblib.load('xgboost_model.joblib')

# Obtener nombres de características
feature_names = ["HighBP", "HighChol", "CholCheck", "BMI", "Smoker", "Stroke", 
                 "HeartDiseaseorAttack", "PhysActivity", "Fruits", "Veggies", 
                 "HvyAlcoholConsump", "AnyHealthcare", "NoDocbcCost", "GenHlth", 
                 "MentHlth", "PhysHlth", "DiffWalk", "Sex", "Age", "Education", "Income"]

# Mostrar gráfico de importancia de características
st.subheader("Importancia de Características")
plot_feature_importance(model, feature_names)
# Instrucciones para configurar la base de datos MySQL:
"""
CREATE DATABASE diabetes_predictions;
USE diabetes_predictions;

CREATE TABLE predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    HighBP INT,
    HighChol INT,
    CholCheck INT,
    BMI FLOAT,
    Smoker INT,
    Stroke INT,
    HeartDiseaseorAttack INT,
    PhysActivity INT,
    Fruits INT,
    Veggies INT,
    HvyAlcoholConsump INT,
    AnyHealthcare INT,
    NoDocbcCost INT,
    GenHlth INT,
    MentHlth INT,
    PhysHlth INT,
    DiffWalk INT,
    Sex INT,
    Age INT,
    Education INT,
    Income INT,
    prediction FLOAT,
    prediction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""