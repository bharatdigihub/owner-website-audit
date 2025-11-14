"""Simple client to call the local model service at runtime."""
import requests
import logging
from typing import List, Any

logger = logging.getLogger(__name__)
MODEL_SERVICE_URL = "http://localhost:8000"

def predict(features: List[Any]):
    url = f"{MODEL_SERVICE_URL}/predict"
    try:
        resp = requests.post(url, json={"features": features}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data
    except Exception as e:
        logger.exception(f"Failed to call model service at {url}")
        return {"pred_label": 0, "probabilities": [1.0, 0.0]}
