
# <img src="src/assets/images/logo-glucosense.png" alt="Logo" style="vertical-align: middle;">
# **Glucosense - Modelo de Concientización sobre Prevención de Diabetes**

---

## **Glucosense**  
**Glucosense** es una aplicación desarrollada para concienciar a la población sobre la importancia de una alimentación saludable en la prevención de enfermedades comunes, como la diabetes. Utilizando un modelo de predicción de machine learning, nuestra herramienta permite identificar el riesgo de desarrollar diabetes basándose en datos de salud. Este proyecto está orientado a fomentar la prevención temprana a través de recomendaciones personalizadas y accesibles.

---

## **Tecnologías Utilizadas**

![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)

---

## **Objetivo del Proyecto**
La diabetes es una de las enfermedades más comunes y prevenibles hoy en día. Mediante la combinación de tecnologías de machine learning y plataformas interactivas, **Glucosense** busca educar a los usuarios sobre la importancia de un estilo de vida saludable y proporcionarles herramientas que les permitan evaluar su riesgo de desarrollar diabetes.

Este proyecto utiliza un **modelo de predicción regresiva** basado en el análisis de indicadores de salud. Estos datos se obtuvieron de la base de datos pública en **Kaggle**:  
[Diabetes Health Indicators Dataset](https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset?select=diabetes_binary_health_indicators_BRFSS2015.csv)

---

## **Video Demostrativo**
A continuación, puedes ver un video explicativo sobre cómo funciona Glucosense.

[Video de Glucosense](./src/assets/videos/demo.mp4)

---

## **Instrucciones de Instalación**

### **Paso 1: Clonar el Repositorio**
Comienza clonando este repositorio en tu máquina local.

```bash
git clone https://github.com/tu_usuario/glucosense.git
cd glucosense
```

### **Paso 2: Crear un Entorno Virtual**
Recomendamos crear un entorno virtual para mantener todas las dependencias del proyecto aisladas.

```bash

# En Linux/MacOS
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
.\venv\Scripts\activate
```

### **Paso 3: Instalar las Dependencias**
Instala todas las dependencias necesarias listadas en el archivo requirements.txt.

```bash
pip install -r requirements.txt
```

### **Paso 4: Configurar AWS**
Este proyecto utiliza servicios en la nube de AWS para el despliegue de modelos y la gestión de datos. Para configurarlo:

Asegúrate de tener una cuenta de AWS.
Configura tus credenciales de AWS:
```bash
aws configure
```

Configura los servicios de AWS necesarios como S3 para almacenamiento de modelos o datos, y Lambda para desplegar funciones, dependiendo de las necesidades del proyecto.
### **Paso 5: Ejecutar el Proyecto Localmente**
Una vez instaladas las dependencias, puedes iniciar la aplicación ejecutando el siguiente comando en tu terminal:

```bash

streamlit run app.py
```

Esto abrirá la aplicación en tu navegador. Desde allí, podrás interactuar con el modelo predictivo y ver los resultados personalizados sobre el riesgo de diabetes.

Arquitectura del Proyecto
Frontend (Streamlit): Una interfaz de usuario interactiva que facilita la introducción de datos y muestra los resultados de la predicción de una forma comprensible y atractiva. El diseño se centra en la simplicidad y la accesibilidad.

Modelo de Machine Learning (Python): El modelo predictivo es una regresión supervisada que evalúa múltiples indicadores de salud, como los niveles de actividad física, hábitos alimenticios y condiciones preexistentes, para estimar el riesgo de diabetes.

Cloud (AWS): Utilizamos servicios en la nube de AWS para almacenar y desplegar nuestro modelo de machine learning, así como para gestionar el almacenamiento de datos y otros recursos necesarios para la operación de la aplicación.

Fuente de Datos
La base de datos utilizada para entrenar el modelo fue obtenida de Kaggle:
Diabetes Health Indicators Dataset

El dataset contiene más de 250,000 registros con variables relacionadas con la salud, como índice de masa corporal (IMC), niveles de actividad física, hábitos de fumar, entre otros factores importantes que influyen en el desarrollo de la diabetes.

Contribuciones
Las contribuciones son bienvenidas. Si deseas colaborar con Glucosense, sigue estos pasos:

Haz un fork de este repositorio.
Crea una rama para tu función (git checkout -b feature/nueva-funcionalidad).
Realiza tus cambios y haz un commit (git commit -am 'Añadida nueva funcionalidad').
Haz push a la rama (git push origin feature/nueva-funcionalidad).
Abre un Pull Request.
Licencia
Este proyecto está bajo la Licencia MIT, lo que significa que eres libre de usar, modificar y distribuir el código, siempre y cuando mantengas los créditos originales y sigas los términos de la licencia.

Contacto
Para más información o preguntas sobre el proyecto, no dudes en ponerte en contacto con nosotros.

© Glucosense 2024. Todos los derechos reservados.