import pickle
import numpy as np
import streamlit as st
import requests
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from sklearn.exceptions import NotFittedError
st.set_page_config(page_title="Predicción de Diabetes", page_icon="🩺", layout="wide")

st.markdown("""
<style>
    body {
        background-color: #e8f5ff;
        color: #fff;
        font-family: 'Arial', sans-serif;
    }

    .stApp {
        background-image: linear-gradient(120deg, #b3e5fc 0%, #e8f5ff 100%);
    }

    .navbar {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: transparent;
        border-radius: 0 0 10px 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    .navbar img {
        height: 50px;
        margin-right: 15px;
    }

    .navbar h1 {
        color: white; 
        margin: 0;
        font-size: 1.5rem;
    }

    input, select {
        background-color: #ffffff;
        border: 1px solid #90caf9;
        padding: 10px;
        font-size: 1rem;
        border-radius: 10px;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
        transition: box-shadow 0.3s ease, border-color 0.3s ease;
    }

    input:hover, select:hover {
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
        border-color: #64b5f6;
    }

    .stButton>button {
        background-color: #2196f3;
        color: white;
        padding: 10px 20px;
        font-size: 1rem;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.3s ease, box-shadow 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #1976d2;
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
    }

    .stSlider>div {
        padding: 10px 0;
    }

    .stSlider>div>div>div>div {
        color: #BFD9EEFF;
        font-weight: bold;
    }

    h1, h2, h3, h4, h5 {
        font-family: 'Arial', sans-serif;
        color: #fff;
    }

    h1 {
        text-align: center;
        font-size: 2.5rem;
        color: #ffffff;
        margin-bottom: 1.5rem;
    }

    img {
        margin: 20px auto;
        display: block;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    .footer {
        text-align: center;
        padding: 15px 0;
        background-color: #2196f3;
        color: white;
        position: relative;
        bottom: 10px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Contenido de la Navbar
with st.container():
    st.markdown('<div class="navbar">', unsafe_allow_html=True)
    st.image("src/assets/images/logo-glucosense.png", use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

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
    conn = sqlite3.connect('diabetes_predictions.db')
    query = "SELECT * FROM predictions ORDER BY id DESC LIMIT 10"
    df = pd.read_sql(query, conn)
    st.dataframe(df)
except sqlite3.Error as e:
    st.error(f"Error al conectar con la base de datos: {e}")
finally:
    if conn:
        conn.close()

def plot_feature_importance(model, feature_names):
    try:
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        plt.figure(figsize=(10,6))
        plt.title("Importancia de Características")
        plt.bar(range(len(importances)), importances[indices])
        plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=90)
        plt.tight_layout()
        st.pyplot(plt)
    except NotFittedError:
        st.error("El modelo no ha sido entrenado. No se puede mostrar la importancia de las características.")
    except Exception as e:
        st.error(f"Error al generar el gráfico de importancia de características: {str(e)}")

# Cargar el modelo
try:
    with open('random_forest_model.pkl', 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    st.error("No se encontró el archivo del modelo 'random_forest_model.pkl'. Asegúrate de que el modelo esté entrenado y guardado correctamente.")
    model = None
except Exception as e:
    st.error(f"Error al cargar el modelo: {str(e)}")
    model = None

# Obtener nombres de características
feature_names = ["HighBP", "HighChol", "CholCheck", "BMI", "Smoker", "Stroke", 
                 "HeartDiseaseorAttack", "PhysActivity", "Fruits", "Veggies", 
                 "HvyAlcoholConsump", "AnyHealthcare", "NoDocbcCost", "GenHlth", 
                 "MentHlth", "PhysHlth", "DiffWalk", "Sex", "Age", "Education", "Income"]

# Mostrar gráfico de importancia de características
st.subheader("Importancia de Características")
if model is not None:
    plot_feature_importance(model, feature_names)
else:
    st.warning("No se puede mostrar la importancia de las características porque el modelo no se cargó correctamente.")

# Footer
st.markdown('<div class="footer">© Glucosense 2024</div>', unsafe_allow_html=True)