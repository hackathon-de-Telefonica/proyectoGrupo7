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


# Formulario de entrada
HighBP = st.selectbox('Presión arterial alta', ['Sí', 'No'])
CholCheck = st.selectbox('Chequeo de colesterol.', ['Sí', 'No'], help='Chequeo en los últimos 5 años.')
HighChol = st.selectbox('Colesterol alto', ['Sí', 'No'])


#BMI = st.number_input('IMC', min_value=0.0, max_value=50.0, value=25.0)
estatura=st.number_input('Estatura (m)', min_value=1.0, max_value=210.0)
peso=st.number_input('Peso (kg)', min_value=0.0)
BMI=round((peso/(estatura)**2),2)
Smoker = st.selectbox('Fumador', ['Sí', 'No'], help='Se considera como fumador haber consumido al menos 100 cigarrillos en su vida.')
Stroke = st.selectbox('Accidente cerebrovascular', ['Sí', 'No'])
HeartDiseaseorAttack = st.selectbox('Enfermedad coronaria o infarto de miocardio', ['Sí', 'No'])
PhysActivity = st.selectbox('Actividad física de forma continuada ', ['Sí', 'No'], help='Durante de 30 días')
Fruits = st.selectbox('Consumo de frutas', ['Sí', 'No'], help='Una o más frutas por día.')
Veggies = st.selectbox('Consumo de verduras', ['Sí', 'No'], help='Una o más verduras por día')
HvyAlcoholConsump = st.selectbox('Consumo de alcohol por semana', ['Sí', 'No'], help='Seleccione "Sí" si su consumo supera Hombre:14 | Mujer:7')
AnyHealthcare = st.selectbox('Tiene seguro de salud', ['Sí', 'No'])
NoDocbcCost = st.selectbox('No ha podido acudir al médico por razones económicas en el último año.', ['Sí', 'No'])

#GenHlth
GenHlth_text = st.selectbox('Salud general', options=['Excelente', 'Muy bien', 'Bien', 'Regular', 'Mal'])
# Convertir el valor seleccionado a su correspondiente numérico
GenHlth = genhlth_map[GenHlth_text]

MentHlth = st.slider('Promedio de días en los que su estado anímico se ha visto afectado.', min_value=0, max_value=30, value=0,help='Ingresa el número promedio de días en que has experimentado problemas de salud mental en el último mes. Incluye stress, depresión.')
PhysHlth = st.slider('Promedio de días en los que su estado físico se ha visto afectado', min_value=0, max_value=30, value=0, help='Ingresa el número promedio de días en que has experimentado problemas de salud física en el último mes. Incluye dolor, enfermedad.')
DiffWalk = st.selectbox('Dificultad respiratoria al caminar o subir escaleras', ['Sí', 'No'])

Sex = st.selectbox('Sexo', ['Mujer', 'Hombre'])

Age = st.slider('Edad', min_value=18, max_value=100, value=30)

# Crear el selectbox con los valores equivalentes
Education_text= st.selectbox('Nivel de educación', options=['Educación primaria', 'Educación básica', 'Educación Secundaria', 'Educación Bachillerato', 'Formación Profesional o Educación superior < 3 años','Educación universitaria y/o superior'])
Education=education_map[Education_text]


Income = st.slider('Nivel de ingresos anuales',  min_value=0, max_value=100000, step=1000, value=24000)
#income_cat = st.slider('Selecciona tu ingreso anual ($)', min_value=0, max_value=100000, step=1000, value=24000)

if st.button('Predecir'):
    # Preparar los datos para la API
    data = {
        "HighBP": convertir_a_binario(HighBP),
        "HighChol": convertir_a_binario(HighChol),
        "CholCheck": convertir_a_binario(CholCheck),
        "BMI": BMI,
        "Smoker": convertir_a_binario(Smoker),
        "Stroke": convertir_a_binario(Stroke),
        "HeartDiseaseorAttack": convertir_a_binario(HeartDiseaseorAttack),
        "PhysActivity": convertir_a_binario(PhysActivity),
        "Fruits":convertir_a_binario(Fruits),
        "Veggies": convertir_a_binario(Veggies),
        "HvyAlcoholConsump": convertir_a_binario(HvyAlcoholConsump),
        "AnyHealthcare": convertir_a_binario(AnyHealthcare),
        "NoDocbcCost": convertir_a_binario(NoDocbcCost),
        "GenHlth":GenHlth,
        "MentHlth": MentHlth,
        "PhysHlth": PhysHlth,
        "DiffWalk": convertir_a_binario(DiffWalk),
        "Sex": convertir_genero(Sex),
        "Age": categorizar_edad(Age),
        "Education": Education,
        "Income": categorizar_ingreso(Income)
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
