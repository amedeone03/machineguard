from datetime import datetime
from functools import lru_cache

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from machineguard.data.ingestion import (
    update_measurement_prediction,
)
from machineguard.models.inference import (
    load_inference_pipeline,
    predict_anomaly,
)


app = FastAPI(
    title="MachineGuard API",
    version="0.1.0",
)


class PredictionRequest(BaseModel):
    bearing_id: int | None = None
    timestamp: datetime | None = None

    rms: float = Field(ge=0)
    std: float = Field(ge=0)
    peak: float = Field(ge=0)
    crest_factor: float = Field(ge=0)
    kurtosis: float
    dominant_frequency: float = Field(ge=0)
    spectral_energy: float = Field(ge=0)


class PredictionResponse(BaseModel):
    anomaly_score: float
    anomaly_flag: bool
    status: str


@lru_cache
def get_inference_pipeline():
    return load_inference_pipeline()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "machineguard",
    }


@app.post(
    "/predict",
    response_model=PredictionResponse,
)
def predict(request: PredictionRequest):
    features = {
        "rms": request.rms,
        "std": request.std,
        "peak": request.peak,
        "crest_factor": request.crest_factor,
        "kurtosis": request.kurtosis,
        "dominant_frequency": request.dominant_frequency,
        "spectral_energy": request.spectral_energy,
    }

    model, scaler, threshold = get_inference_pipeline()

    prediction = predict_anomaly(
        features=features,
        model=model,
        scaler=scaler,
        threshold=threshold,
    )

    if (
        request.bearing_id is not None
        and request.timestamp is not None
    ):
        updated_rows = update_measurement_prediction(
            bearing_id=request.bearing_id,
            timestamp=request.timestamp,
            anomaly_score=prediction["anomaly_score"],
            anomaly_flag=prediction["anomaly_flag"],
        )

        if updated_rows == 0:
            raise HTTPException(
                status_code=404,
                detail="Measurement not found.",
            )

    prediction["status"] = (
        "ANOMALOUS"
        if prediction["anomaly_flag"]
        else "NORMAL"
    )

    return prediction