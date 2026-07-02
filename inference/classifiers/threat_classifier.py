from typing import Optional, Tuple
import numpy as np


THREAT_CLASSES = {
    0: "DDoS",
    1: "Botnet",
    2: "Unauthorized",
    3: "MitM",
    4: "Ransomware",
    5: "Scanning",
    6: "Unknown",
}

CLASS_IDS = {v: k for k, v in THREAT_CLASSES.items()}

THREAT_CLASSIFIER_INPUT_FEATURES = list(range(0, 12)) + list(range(18, 29)) + list(range(38, 44))


class ThreatClassifier:
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path
        self._model = None

    def load_model(self, model_path: str):
        try:
            import joblib
            self._model = joblib.load(model_path)
            self.model_path = model_path
        except Exception:
            self._model = None

    def train(self, X: np.ndarray, y: np.ndarray):
        import xgboost as xgb
        self._model = xgb.XGBClassifier(
            n_estimators=200,
            max_depth=8,
            learning_rate=0.1,
            objective='multi:softprob',
            num_class=7,
            random_state=42,
            eval_metric='mlogloss',
        )
        self._model.fit(X, y)

    def predict(self, feature_vector: np.ndarray) -> Tuple[str, float]:
        if self._model is None:
            return "Unknown", 0.0
        selected = feature_vector[THREAT_CLASSIFIER_INPUT_FEATURES]
        selected = selected.reshape(1, -1)
        probs = self._model.predict_proba(selected)[0]
        best_idx = int(np.argmax(probs))
        confidence = float(probs[best_idx])
        if confidence < 0.6:
            return "Unknown", confidence
        return THREAT_CLASSES.get(best_idx, "Unknown"), confidence

    def predict_proba(self, feature_vector: np.ndarray) -> dict:
        if self._model is None:
            return {"Unknown": 1.0}
        selected = feature_vector[THREAT_CLASSIFIER_INPUT_FEATURES]
        selected = selected.reshape(1, -1)
        probs = self._model.predict_proba(selected)[0]
        return {THREAT_CLASSES[i]: float(probs[i]) for i in range(len(probs))}

    def save_model(self, model_path: str):
        if self._model is not None:
            import joblib
            joblib.dump(self._model, model_path)
            self.model_path = model_path

    @property
    def is_loaded(self) -> bool:
        return self._model is not None
