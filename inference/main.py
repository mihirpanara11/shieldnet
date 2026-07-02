from typing import Optional
import time
import uuid
import logging

from inference.ensemble import fuse_scores, classify_decision, requires_airo
from inference.models.lstm_runner import LSTMRunner
from inference.models.isolation_forest_runner import IsolationForestRunner
from inference.models.autoencoder_runner import AutoencoderRunner
from inference.classifiers.threat_classifier import ThreatClassifier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("shieldnet.inference")


class InferenceEngine:
    def __init__(self, model_path: str = "/models", model_version: str = "global-v1",
                 threshold_low: float = 0.40, threshold_high: float = 0.70):
        self.model_path = model_path
        self.model_version = model_version
        self.threshold_low = threshold_low
        self.threshold_high = threshold_high
        self.lstm_runners: dict = {}
        self.if_runners: dict = {}
        self.ae_runners: dict = {}
        self.classifier = ThreatClassifier()
        self._lstm_weights: Optional[list] = None
        self._ae_weights: Optional[list] = None
        self.last_fl_update: Optional[str] = None

    def get_lstm_runner(self, category: str) -> LSTMRunner:
        if category not in self.lstm_runners:
            self.lstm_runners[category] = LSTMRunner()
            model_file = f"{self.model_path}/lstm_{category}_{self.model_version}.keras"
            try:
                self.lstm_runners[category].load_model(model_file)
            except Exception:
                pass
        return self.lstm_runners[category]

    def get_if_runner(self, device_id: str) -> IsolationForestRunner:
        if device_id not in self.if_runners:
            self.if_runners[device_id] = IsolationForestRunner()
            model_file = f"{self.model_path}/if_{device_id}.pkl"
            try:
                self.if_runners[device_id].load_model(model_file)
            except Exception:
                pass
        return self.if_runners[device_id]

    def get_ae_runner(self, category: str) -> AutoencoderRunner:
        if category not in self.ae_runners:
            self.ae_runners[category] = AutoencoderRunner()
            model_file = f"{self.model_path}/ae_{category}_{self.model_version}.keras"
            try:
                self.ae_runners[category].load_model(model_file)
            except Exception:
                pass
        return self.ae_runners[category]

    def infer(self, device_id: str, zone_id: str, category: str,
              feature_vector: list, protocol: str = "MQTT") -> dict:
        import numpy as np
        start_time = time.time()
        fv = np.array(feature_vector, dtype=np.float32)

        lstm_runner = self.get_lstm_runner(category)
        lstm_score = lstm_runner.predict(fv)

        if_runner = self.get_if_runner(device_id)
        if_score = if_runner.predict(fv)

        ae_runner = self.get_ae_runner(category)
        ae_score = ae_runner.predict(fv)

        ensemble_score = fuse_scores(lstm_score, if_score, ae_score)
        decision = classify_decision(ensemble_score)

        threat_class = "Unknown"
        threat_confidence = 0.0
        if ensemble_score >= self.threshold_low:
            threat_class, threat_confidence = self.classifier.predict(fv)

        inference_time_ms = int((time.time() - start_time) * 1000)

        result = {
            "device_id": device_id,
            "zone_id": zone_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.") + f"{int(time.time()*1000)%1000:03d}Z",
            "score_lstm": round(float(lstm_score), 4),
            "score_if": round(float(if_score), 4),
            "score_ae": round(float(ae_score), 4),
            "score_ensemble": ensemble_score,
            "decision": decision,
            "threat_class": threat_class,
            "threat_confidence": round(threat_confidence, 4),
            "model_version": self.model_version,
            "inference_time_ms": inference_time_ms,
        }
        return result

    def update_global_weights(self, lstm_weights: list, ae_weights: list,
                              model_version: str, classifier_path: Optional[str] = None):
        self._lstm_weights = lstm_weights
        self._ae_weights = ae_weights
        self.model_version = model_version
        for category, runner in self.lstm_runners.items():
            runner.load_weights(lstm_weights)
        for category, runner in self.ae_runners.items():
            runner.load_weights(ae_weights)
        if classifier_path:
            self.classifier.load_model(classifier_path)
        self.last_fl_update = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        logger.info(f"Model updated to {model_version}")
