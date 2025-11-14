"""Model wrapper for PyTorch with a fallback stub predictor."""
import os
import logging

try:
    import torch
    TORCH_AVAILABLE = True
except Exception:
    TORCH_AVAILABLE = False

logger = logging.getLogger(__name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'issue_classifier.pt')

class TorchModelWrapper:
    def __init__(self, device=None):
        self.device = device or ('cuda' if TORCH_AVAILABLE and torch.cuda.is_available() else 'cpu')
        self.model = None
        self.loaded = False

    def load(self, path=MODEL_PATH):
        if not TORCH_AVAILABLE:
            logger.warning('PyTorch not available — using fallback stub predictor')
            self.loaded = False
            return

        if not os.path.exists(path):
            logger.warning(f'Model file not found at {path} — using stub predictor')
            self.loaded = False
            return

        try:
            # Try to load TorchScript first, then state dict
            try:
                self.model = torch.jit.load(path, map_location=self.device)
            except Exception:
                self.model = torch.load(path, map_location=self.device)
            self.model.eval()
            self.loaded = True
            logger.info(f'Model loaded from {path} onto {self.device}')
        except Exception as e:
            logger.exception('Failed to load model, falling back to stub predictor')
            self.loaded = False

    def predict(self, features):
        """
        Predict method accepts a list or nested list of numeric features and returns
        a dict {pred_label: int, probabilities: [float]}
        If PyTorch is not available or model not loaded, returns a deterministic stub.
        """
        # Simple stub: sum features and threshold
        try:
            if not TORCH_AVAILABLE or not self.loaded:
                s = 0
                for v in features:
                    if isinstance(v, (list, tuple)):
                        s += sum([float(x) for x in v])
                    else:
                        s += float(v)
                # deterministic pseudo prediction based on sum
                pred = 1 if s > 10 else 0
                probs = [0.4, 0.6] if pred == 1 else [0.7, 0.3]
                return {'pred_label': int(pred), 'probabilities': probs}

            import numpy as np
            import torch
            arr = np.array(features, dtype=np.float32)
            if arr.ndim == 1:
                arr = arr.reshape(1, -1)
            tensor = torch.from_numpy(arr).to(self.device)
            with torch.no_grad():
                outputs = self.model(tensor)
                if outputs.ndim == 1:
                    outputs = outputs.unsqueeze(0)
                probs = torch.softmax(outputs, dim=1).cpu().numpy().tolist()[0]
                pred = int(np.argmax(probs))
                return {'pred_label': pred, 'probabilities': probs}
        except Exception as e:
            logger.exception('Error during prediction — returning stub result')
            return {'pred_label': 0, 'probabilities': [1.0, 0.0]}
