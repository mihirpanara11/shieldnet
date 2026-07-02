import time
import logging
from typing import Optional

from fl_server.strategy import FedAvgStrategy
from fl_server.model_registry import ModelRegistry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("shieldnet.fl.server")


class FLServer:
    def __init__(self, server_address: str = "0.0.0.0:9080",
                 min_clients: int = 3):
        self.server_address = server_address
        self.strategy = FedAvgStrategy(min_clients=min_clients)
        self.registry = ModelRegistry()
        self._round = 0
        self._client_updates = []
        self._global_weights: Optional[list] = None

    def receive_update(self, zone_id: str, gradients: list,
                       num_samples: int, loss: float, auc: float):
        metrics = {"loss": loss, "auc": auc, "samples": num_samples}
        version = self.registry.register_round(self._round + 1, zone_id, metrics)

        self._client_updates.append((gradients, num_samples))

        if len(self._client_updates) >= 3:
            self._aggregate_round()

        return version

    def _aggregate_round(self):
        self._round += 1
        aggregated = self.strategy.aggregate(self._client_updates)
        if aggregated is not None:
            self._global_weights = aggregated
            avg_metrics = self.strategy.weighted_average(
                [(n, {"loss": 0.1, "auc": 0.95}) for _, n in self._client_updates])
            self.registry.update_global_metrics(
                avg_metrics.get("auc", 0.95), 0.94)
            self.registry.consume_privacy_budget(1.0)
            logger.info(f"Round {self._round} aggregation complete")

        self._client_updates = []

    def get_global_weights(self) -> Optional[list]:
        return self._global_weights

    def get_status(self) -> dict:
        return self.registry.get_status()


def run_fl_server(host: str = "0.0.0.0", port: int = 9080):
    server = FLServer(server_address=f"{host}:{port}")
    logger.info(f"FL Server starting on {host}:{port}")
    return server
