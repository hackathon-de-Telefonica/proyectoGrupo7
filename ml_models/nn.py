import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold, RandomizedSearchCV
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from scikeras.wrappers import KerasClassifier
import joblib

# 1. Preparar el dataset completo
diabetes_df = pd.read_csv('diabetes.csv')

X = diabetes_df.drop('Diabetes_binary', axis=1)
y = diabetes_df['Diabetes_binary']

# Convertir las columnas categóricas a variables dummy (si es necesario)
X = pd.get_dummies(X, drop_first=True)

# 2. Escalar los datos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. Tomar una muestra de 20,000 casos para la búsqueda de hiperparámetros
X_sample, _, y_sample, _ = train_test_split(X_scaled, y, train_size=20000, stratify=y, random_state=42)

# 4. Definir el modelo de la red neuronal
def crear_modelo(units=32, activation='relu', optimizer='adam'):
    model = Sequential()
    model.add(Dense(units, input_dim=X_sample.shape[1], activation=activation))
    model.add(Dense(units//2, activation=activation))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
    return model

# 5. Crear el KerasClassifier con los hiperparámetros predeterminados
modelo = KerasClassifier(
    model=crear_modelo, 
    epochs=10, 
    batch_size=32, 
    verbose=0
)

# Definir los hiperparámetros a buscar
parametros = {
    'model__units': [16, 32, 64],                   # Neuronas en la capa oculta
    'model__activation': ['relu', 'tanh'],          # Función de activación
    'model__optimizer': ['adam', 'sgd'],            # Optimizadores
    'batch_size': [16, 32, 64],                     # Tamaño de batch
    'epochs': [10, 20]                              # Número de épocas
}

# 6. Búsqueda de hiperparámetros con RandomizedSearchCV
random_search = RandomizedSearchCV(estimator=modelo, param_distributions=parametros, n_iter=10, cv=3, verbose=1, n_jobs=-1)
random_search.fit(X_sample, y_sample)

# Mostrar los mejores hiperparámetros encontrados
print("Mejores hiperparámetros encontrados:")
print(random_search.best_params_)

# 7. Ahora, aplicar estos hiperparámetros al dataset completo con validación cruzada
best_params = random_search.best_params_

# Crear el modelo con los mejores hiperparámetros
def crear_mejor_modelo():
    model = Sequential()
    model.add(Dense(best_params['model__units'], input_dim=X_scaled.shape[1], activation=best_params['model__activation']))
    model.add(Dense(best_params['model__units']//2, activation=best_params['model__activation']))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer=best_params['model__optimizer'], loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Hacer validación cruzada con el dataset completo
kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
predicciones_cruzadas = np.zeros(len(y))  # Para almacenar predicciones

for train_idx, test_idx in kfold.split(X_scaled, y):
    X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    
    # Crear y entrenar el modelo con los mejores hiperparámetros
    mejor_modelo = crear_mejor_modelo()
    mejor_modelo.fit(X_train, y_train, epochs=best_params['epochs'], batch_size=best_params['batch_size'], verbose=0)
    
    # Predecir las clases en el conjunto de prueba
    predicciones_cruzadas[test_idx] = mejor_modelo.predict(X_test).flatten()

# Convertir las predicciones continuas en predicciones binarias (0 o 1)
y_pred = (predicciones_cruzadas > 0.5).astype(int)

# 8. Evaluar el modelo con la matriz de confusión
print("Matriz de confusión (validación cruzada con mejores hiperparámetros):")
print(confusion_matrix(y, y_pred))

print("\nInforme de clasificación:")
print(classification_report(y, y_pred))

# 9. Precisión final del modelo
accuracy = accuracy_score(y, y_pred)
print(f"Precisión del modelo en el dataset completo: {accuracy:.2f}")

# Guardar el modelo en un archivo
joblib.dump(mejor_modelo, 'models_ml/pkls/nn_model.pkl')
print("Modelo guardado como nn_model.pkl")