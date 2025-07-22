from pydantic import BaseModel, Field, field_validator
from typing import Literal
import unicodedata

class PredictionInput(BaseModel):
    """
    Modelo de validación para los datos de entrada del modelo.
    Las variables numéricas deben estar entre 0 y 100.
    El documento dice 0 y 1 sin embargo el data set indica min 0 max 100
    """
    uso_cpu: float = Field(..., ge=0.0, le=100.0)
    uso_memoria: float = Field(..., ge=0.0, le=100.0)
    tiempo_ejecucion: float = Field(..., ge=0.0, le=100.0)
    tipo_proceso: Literal["aplicacion", "servicio", "sistema"]

    @field_validator("tipo_proceso", mode="before")
    @classmethod
    def normalizar_tipo(cls, v):
        # Quita tildes y convierte a minúsculas
        v = unicodedata.normalize('NFKD', v).encode('ASCII', 'ignore').decode('utf-8').lower()
        return v

