from typing import Optional
import numpy as np
import joblib


class IsolationForestRunner:
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path
        self._model = None

    def load_model(self, model_path: str):
        try:
            self._model = joblib.load(model_path)
            self.model_path = model_path
        except Exception:
            self._model = None

    def train(self, X: np.ndarray):
        from sklearn.ensemble import IsolationForest
        n_samples = len(X)
        self._model = IsolationForest(
            n_estimators=200,
            max_samples=min(256, n_samples) if n_samples > 0 else 'auto',
            contamination=0.05,
            max_features=1.0,
            bootstrap=False,
            random_state=42,
        )
        self._model.fit(X)

    def predict(self, feature_vector: np.ndarray) -> float:
        if self._model is None:
            return 0.0
        feature_vector = feature_vector.reshape(1, -1)
        raw_score = self._model.decision_function(feature_vector)[0]
        normalized = 1.0 - (raw_score + 0.5)
        return float(np.clip(normalized, 0.0, 1.0))

    def save_model(self, model_path: str):
        if self._model is not None:
            joblib.dump(self._model, model_path)
            self.model_path = model_path

    @property
    def is_loaded(self) -> bool:
        return self._model is not None
