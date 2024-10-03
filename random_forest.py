import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle


# Cargar los datos
data = pd.read_csv('diabetes.csv')  # Asegúrate de que el archivo CSV esté en el directorio correcto

# Separar características y variable objetivo
X = data.drop('Diabetes_binary', axis=1)
y = data['Diabetes_binary']

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Escalar las características
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Entrenar el modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluar el modelo
train_score = model.score(X_train_scaled, y_train)
test_score = model.score(X_test_scaled, y_test)

print(f"Precisión en entrenamiento: {train_score:.4f}")
print(f"Precisión en prueba: {test_score:.4f}")

# Guardar el modelo y el scaler
with open('random_forest_model.pkl', 'wb') as file:
    pickle.dump(model, file)

with open('scaler.pkl', 'wb') as file:
    pickle.dump(scaler, file)

print("Modelo y scaler guardados como archivos .pkl")