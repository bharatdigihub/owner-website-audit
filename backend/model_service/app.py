"""FastAPI model service exposing a /predict endpoint."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Any
import logging
from .predictor import TorchModelWrapper

logger = logging.getLogger('model_service')
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Website Analyzer Model Service", version="0.1")

# Initialize model wrapper (load lazily)
MODEL = TorchModelWrapper()
MODEL.load()

class PredictRequest(BaseModel):
    features: List[Any]

class PredictResponse(BaseModel):
    pred_label: int
    probabilities: List[float]

@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": MODEL.loaded}

@app.post("/predict", response_model=PredictResponse)
async def predict(req: PredictRequest):
    try:
        if not req.features:
            raise HTTPException(status_code=400, detail="No features provided")
        result = MODEL.predict(req.features)
        return PredictResponse(pred_label=int(result.get('pred_label', 0)), probabilities=result.get('probabilities', []))
    except HTTPException:
        raise
    except Exception as e:
        logger.exception('Prediction failed')
        raise HTTPException(status_code=500, detail=str(e))
