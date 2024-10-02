import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, classification_report
from imblearn.combine import SMOTEENN 
from xgboost import XGBClassifier
import joblib

# Cargar los datos
df = pd.read_csv('diabetes.csv')

# Separar características y objetivo
X = df.drop('Diabetes_binary', axis=1)
y = df['Diabetes_binary']

# Dividir en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Escalar las características
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Aplicar SMOTEENN para balance de clases
smoteenn = SMOTEENN(random_state=42)
X_train_resampled, y_train_resampled = smoteenn.fit_resample(X_train_scaled, y_train)

# Definir el modelo XGBoost
model = XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=4,
    min_child_weight=6,
    gamma=0,
    subsample=0.8,
    colsample_bytree=0.8,
    objective='binary:logistic',
    nthread=4,
    scale_pos_weight=1,
    seed=27
)

# Entrenamiento con validación cruzada estratificada
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
for fold, (train_index, val_index) in enumerate(skf.split(X_train_resampled, y_train_resampled), 1):
    print(f'Fold {fold}')
    X_train_fold, X_val_fold = X_train_resampled[train_index], X_train_resampled[val_index]
    y_train_fold, y_val_fold = y_train_resampled[train_index], y_train_resampled[val_index]
    
    model.fit(X_train_fold, y_train_fold, 
              eval_set=[(X_val_fold, y_val_fold)],
              eval_metric='auc',
              early_stopping_rounds=10,
              verbose=False)
    
    print(f'Best iteration: {model.best_iteration}')

# Evaluación final en el conjunto de prueba
y_pred = model.predict(X_test_scaled)
print("Matriz de confusión (conjunto de prueba):")
print(confusion_matrix(y_test, y_pred))
print("\nInforme de clasificación (conjunto de prueba):")
print(classification_report(y_test, y_pred))

# Guardar el modelo y el scaler
joblib.dump(model, 'xgboost_model.joblib')
joblib.dump(scaler, 'scaler.joblib')