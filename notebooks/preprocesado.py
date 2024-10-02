
""" import sys
import os

# Agregar el directorio raíz al PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Ahora puedes importar load_data.py desde scripts
from scripts.load_data import df

# Usar el DataFrame df en el preprocesado
print(df.head())  # Muestra las primeras filas del DataFrame


#from pandas_profiling import ProfileReport
from ydata_profiling import ProfileReport


# Cargar un DataFrame

# Generar un reporte
profile = ProfileReport(df, title="Reporte Exploratorio")
ruta="C:/4_F5/015_hackaton/proyectoGrupo7/outputs/graphs/"
profile.to_file(ruta+"reporte_eda.html")

 """

 
import sys
import os 
 
# Agregar el directorio raíz al PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Importar la función load_data desde scripts/load_data.py
from scripts.load_data import load_data

# Definir la ruta del archivo CSV
data_file = os.path.join(project_root, "data", "raw", "diabetes_binary_5050.csv")

# Llamar a load_data para cargar el DataFrame
df = load_data(data_file)

# Verificar si los datos se cargaron correctamente
if df is not None:
    print(df.head())  # Mostrar las primeras filas del DataFrame

    # Generar un reporte con ydata_profiling
    from ydata_profiling import ProfileReport

    # Crear el perfil
    profile = ProfileReport(df, title="Reporte Exploratorio")

    # Definir la ruta de salida para el reporte
    output_path = os.path.join(project_root, "outputs", "graphs", "reporte_eda.html")

    # Guardar el reporte
    profile.to_file(output_path)
    print(f"Reporte guardado en {output_path}")
else:
    print("Error al cargar los datos.")