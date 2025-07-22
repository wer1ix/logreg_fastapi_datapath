# API para predecir procesos problemáticos en un servidor

Este proyecto consiste en una API RESTful construida con FastAPI que expone un modelo de regresión logística previamente entrenado. El objetivo es predecir si un proceso en ejecución va a ser problemático o no, según su consumo de recursos y tipo.

---

## Estructura del proyecto
```
/app
├── controllers/
│   └── prediction_controllers.py  # validación de entrada
├── models/
│   └── models.py                  # carga del modelo .pkl
├── main.py                           # definición de la app y endpoints
├── model.pkl                         # modelo de regresión logística
requirements.txt
Dockerfile
```

---

## Endpoints implementados

- `POST /predict`: Recibe datos de un proceso y devuelve si es problemático o no
- `GET /predictions`: Muestra el historial completo de predicciones
- `GET /predictions/{id}`: Devuelve la predicción según un id
- `PUT /predict/{id}`: Actualiza los datos de una predicción existente
- `DELETE /delete/{id}`: Elimina una predicción del historial

---

## Requisitos

Este proyecto usa Python 3.11. Las dependencias están en `requirements.txt`:

```
fastapi
uvicorn
pydantic
scikit-learn
pandas
```

---

## Cómo correrlo con Docker

1. Asegúrate de tener Docker corriendo

2. Desde la raíz del proyecto, construye la imagen:
```bash
docker build -t fastapi-model-app .
```

3. Luego corre el contenedor:
```bash
docker run -p 8000:8000 fastapi-model-app
```

4. Abre tu navegador en: `http://localhost:8000/docs`

---

## Ejemplo de entrada (POST /predict)
```json
{
  "uso_cpu": 65.0,
  "uso_memoria": 72.5,
  "tiempo_ejecucion": 50.0,
  "tipo_proceso": "Aplicación"
}
```

---

## Notas
- El modelo fue entrenado con scikit-learn y serializado con pickle
- Se usa un diccionario en memoria para guardar el historial
- No hay base de datos en este proyecto (es solo para propósito educativo)

---

## Pendientes / cosas a mejorar
- Hacer troubleshooting
- Agregar logging para ver errores con más detalle
- Mejorar robustez del manejo de columnas al hacer predicciones
- Posiblemente rehacer la serialización del modelo con joblib o en el mismo entorno que la API

