from typing import Dict, Optional, List
import time
import logging

logger = logging.getLogger("shieldnet.fl.model_registry")


class ModelRegistry:
    def __init__(self, storage_path: str = "/models"):
        self.storage_path = storage_path
        self._models: Dict[str, dict] = {}
        self._global_version = 0
        self._current_round = 0
        self._global_auc_roc = 0.0
        self._global_f1 = 0.0
        self._privacy_epsilon_consumed = 0.0
        self._privacy_epsilon_budget = 1000.0
        self._participations: Dict[str, dict] = {}

    def register_round(self, round_number: int, zone_id: str,
                       metrics: dict) -> str:
        model_version = f"global-v{round_number}"
        self._current_round = round_number
        self._global_version = round_number
        self._participations[zone_id] = {
            "round": round_number,
            "loss": metrics.get("loss", 0),
            "auc": metrics.get("auc", 0),
            "samples": metrics.get("samples", 0),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        return model_version

    def update_global_metrics(self, auc_roc: float, f1: float):
        self._global_auc_roc = auc_roc
        self._global_f1 = f1

    def consume_privacy_budget(self, epsilon: float = 1.0):
        self._privacy_epsilon_consumed += epsilon

    def get_status(self) -> dict:
        return {
            "current_round": self._current_round,
            "global_model_version": f"global-v{self._global_version}",
            "last_aggregation": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "next_aggregation": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() + 3600)),
            "participating_zones": len(self._participations),
            "global_auc_roc": round(self._global_auc_roc, 4),
            "global_f1": round(self._global_f1, 4),
            "privacy_epsilon_consumed": round(self._privacy_epsilon_consumed, 1),
            "privacy_epsilon_budget": self._privacy_epsilon_budget,
        }

    def get_participations(self) -> Dict[str, dict]:
        return self._participations
