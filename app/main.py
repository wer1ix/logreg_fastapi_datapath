from fastapi import FastAPI, HTTPException
from app.controllers.prediction_controllers import PredictionInput
from app.models.models import load_model
import pandas as pd
import uuid

app = FastAPI(title="API para predecir procesos problemáticos")

# Cargar modelo
modelo = load_model()

# Historial de predicciones (en memoria)
historial_predicciones = {}

# Diccionario para traducir la predicción
pred_meaning = {
    0: "Proceso normal",
    1: "Proceso potencialmente problemático"
}

def procesar_input(data: dict):
    df = pd.DataFrame([data])
    # normalizar nombres de columnas
    df.columns = df.columns.str.lower().str.strip()
    tipo = df["tipo_proceso"].iloc[0]

    df["tipo_proceso_servicio"] = 1 if tipo == "servicio" else 0
    df["tipo_proceso_sistema"] = 1 if tipo == "sistema" else 0
    
    # OneHot manual: La columna "tipo_proceso_aplicacion" no es necesaria 
    # porque se eliminó con drop_first=True al hacer One-Hot Encoding (es la categoría base).
    df.drop(columns=["tipo_proceso"], inplace=True)
    
    columnas_finales = [
        "uso_cpu", "uso_memoria", "tiempo_ejecucion",
        "tipo_proceso_servicio", "tipo_proceso_sistema"
    ]

    for col in columnas_finales:
        if col not in df.columns:
            df[col] = 0

    return df[columnas_finales]

@app.post("/predict")
def predecir_proceso(data: PredictionInput):
    entrada = data.dict()
    df = procesar_input(entrada)

    # Predicción
    pred = int(modelo.predict(df)[0])
    prob = round(float(modelo.predict_proba(df)[0][1]), 4)

    # Generar ID y guardar en historial
    pred_id = str(uuid.uuid4())
    historial_predicciones[pred_id] = {
        "entrada": entrada,
        "prediccion": pred,
        "significado": pred_meaning[pred],
        "probabilidad": prob
    }

    return {
        "id": pred_id,
        "prediccion": pred,
        "significado": pred_meaning[pred],
        "probabilidad": prob
    }

@app.get("/predictions")
def obtener_historial():
    return historial_predicciones

@app.get("/predictions/{id}")
def obtener_prediccion(id: str):
    if id not in historial_predicciones:
        raise HTTPException(status_code=404, detail="ID no encontrado")
    return historial_predicciones[id]

@app.put("/predict/{id}")
def actualizar_prediccion(id: str, data: PredictionInput):
    if id not in historial_predicciones:
        raise HTTPException(status_code=404, detail="ID no encontrado")
    entrada = data.dict()
    df = procesar_input(entrada)
    pred = int(modelo.predict(df)[0])
    prob = round(float(modelo.predict_proba(df)[0][1]), 4)
    historial_predicciones[id] = {
        "entrada": entrada,
        "prediccion": pred,
        "significado": pred_meaning[pred],
        "probabilidad": prob
    }
    return {
        "id": id,
        "prediccion": pred,
        "significado": pred_meaning[pred],
        "probabilidad": prob
    }

@app.delete("/delete/{id}")
def eliminar_prediccion(id: str):
    if id not in historial_predicciones:
        raise HTTPException(status_code=404, detail="ID no encontrado")
    del historial_predicciones[id]
    return {"mensaje": f"Predicción con ID {id} eliminada correctamente"}