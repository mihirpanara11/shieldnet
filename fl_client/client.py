import numpy as np
from typing import Dict, Optional, Tuple
import logging

import flwr as fl

from fl_client.local_trainer import LocalTrainer
from fl_client.dp_noise import apply_dp_noise, compute_gradient_delta

logger = logging.getLogger("shieldnet.fl.client")


class FLClient(fl.client.NumPyClient):
    def __init__(self, zone_id: str, local_epochs: int = 3):
        super().__init__()
        self.zone_id = zone_id
        self.trainer = LocalTrainer(local_epochs=local_epochs)
        self._local_data: Dict[str, Tuple[np.ndarray, np.ndarray]] = {}
        self._global_weights: Optional[list] = None

    def load_local_data(self, X: np.ndarray, y: np.ndarray):
        self._local_data["X"] = X
        self._local_data["y"] = y
        logger.info(f"Loaded {len(X)} local training samples")

    def set_global_weights(self, weights: list):
        self._global_weights = weights
        self.trainer.set_weights(weights)

    def get_parameters(self, config) -> list:
        weights = self.trainer.get_weights()
        if weights is None:
            return []
        return weights

    def fit(self, parameters, config) -> Tuple[list, int, dict]:
        self.trainer.set_weights(parameters)
        result = self.train_local()
        return self.trainer.get_weights(), result.get("samples", 0), result

    def evaluate(self, parameters, config) -> Tuple[float, int, dict]:
        self.trainer.set_weights(parameters)
        X = self._local_data.get("X")
        y = self._local_data.get("y")
        if X is None or y is None:
            return 0.0, 0, {"loss": 0.0, "auc": 0.0}
        split = int(len(X) * 0.85)
        _, X_val = X[:split], X[split:]
        _, y_val = y[:split], y[split:]
        if len(X_val) == 0:
            return 0.0, 0, {"loss": 0.0, "auc": 0.0}
        loss, auc = self.trainer.evaluate(X_val, y_val)
        return float(loss), len(X_val), {"loss": float(loss), "auc": float(auc)}

    def train_local(self) -> dict:
        X = self._local_data.get("X")
        y = self._local_data.get("y")
        if X is None or y is None:
            return {"loss": 0.0, "auc": 0.0, "samples": 0}

        split = int(len(X) * 0.85)
        X_train, X_val = X[:split], X[split:]
        y_train, y_val = y[:split], y[split:]

        result = self.trainer.train(X_train, y_train, X_val, y_val)
        logger.info(f"Local training complete - loss: {result['loss']:.4f}, "
                     f"auc: {result['auc']:.4f}, samples: {result['samples']}")
        return result

    def get_gradients(self, global_weights: list) -> Tuple[list, int]:
        local_weights = self.trainer.get_weights()
        if local_weights is None or global_weights is None:
            return [], 0

        delta = compute_gradient_delta(local_weights, global_weights)
        num_samples = len(self._local_data.get("X", []))
        noisy_delta = apply_dp_noise(delta, num_samples)
        return noisy_delta, num_samples

    def get_num_samples(self) -> int:
        return len(self._local_data.get("X", []))
