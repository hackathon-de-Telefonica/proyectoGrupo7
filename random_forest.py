import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# 1. Cargar el dataset
diabetes_df = pd.read_csv('diabetes.csv')

# 2. Tomar una muestra de 20,000 casos solo para la búsqueda de hiperparámetros
df_sample = diabetes_df.sample(n=20000, random_state=42)

# 3. Preparar los datos de la muestra
X_sample = df_sample.drop('Diabetes_binary', axis=1)
y_sample = df_sample['Diabetes_binary']

# Convertir las columnas categóricas en variables dummy (si es necesario)
X_sample = pd.get_dummies(X_sample, drop_first=True)

# 4. Escalar los datos
scaler = StandardScaler()
X_sample_scaled = scaler.fit_transform(X_sample)

# 5. Definir el modelo y los hiperparámetros a buscar
model = RandomForestClassifier(random_state=42)

# Espacio de búsqueda de hiperparámetros
param_grid = {
    'n_estimators': [100, 200],  
    'max_depth': [None, 10, 20], 
    'min_samples_split': [2, 5], 
    'min_samples_leaf': [1, 2]
}

# 6. Búsqueda de hiperparámetros usando la muestra
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='accuracy', verbose=1, n_jobs=-1)
grid_search.fit(X_sample_scaled, y_sample)

# 7. Obtener los mejores hiperparámetros
best_params = grid_search.best_params_
print(f"Mejores hiperparámetros encontrados: {best_params}")

# 8. Ahora, entrenar con todo el dataset usando los mejores hiperparámetros
X_full = diabetes_df.drop('Diabetes_binary', axis=1)
y_full = diabetes_df['Diabetes_binary']

# Convertir columnas categóricas a variables dummy
X_full = pd.get_dummies(X_full, drop_first=True)

# Escalar los datos del dataset completo
X_full_scaled = scaler.fit_transform(X_full)

# Definir el mejor modelo con los hiperparámetros encontrados
best_model = RandomForestClassifier(**best_params, random_state=42)

# Validación cruzada con el dataset completo
cv_scores = cross_val_score(best_model, X_full_scaled, y_full, cv=5)

print(f"Puntuaciones de validación cruzada: {cv_scores}")
print(f"Precisión media: {cv_scores.mean():.2f}")

# 9. Entrenar el modelo final con todo el dataset completo
best_model.fit(X_full_scaled, y_full)

# 10. Evaluar el modelo usando la matriz de confusión
y_pred_full = best_model.predict(X_full_scaled)
print("Matriz de confusión (dataset completo):")
print(confusion_matrix(y_full, y_pred_full))

print("\nInforme de clasificación (dataset completo):")
print(classification_report(y_full, y_pred_full))

# 11. Precisión final del modelo
accuracy = accuracy_score(y_full, y_pred_full)
print(f"Precisión del modelo en el dataset completo: {accuracy:.2f}")

# Guardar el modelo y el scaler
joblib.dump(model, 'random_forest.joblib')
joblib.dump(scaler, 'scaler.joblib')