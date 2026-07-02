from typing import List, Tuple, Optional
import numpy as np
import logging

logger = logging.getLogger("shieldnet.fl.strategy")


class FedAvgStrategy:
    def __init__(self, min_clients: int = 3):
        self.min_clients = min_clients

    def aggregate(self, client_updates: List[Tuple[List[np.ndarray], int]]) -> Optional[List[np.ndarray]]:
        if len(client_updates) < self.min_clients:
            logger.warning(f"Not enough clients: {len(client_updates)} < {self.min_clients}")
            return None

        total_samples = sum(n for _, n in client_updates)
        if total_samples == 0:
            return None

        weights = [w for w, _ in client_updates]
        sample_counts = [n for _, n in client_updates]

        aggregated = []
        for layer_idx in range(len(weights[0])):
            layer_sum = np.zeros_like(weights[0][layer_idx], dtype=np.float64)
            for client_idx, w in enumerate(weights):
                weight = sample_counts[client_idx] / total_samples
                layer_sum += weight * w[layer_idx].astype(np.float64)
            aggregated.append(layer_sum.astype(np.float32))

        logger.info(f"Aggregated {len(client_updates)} client updates, "
                     f"{total_samples} total samples")
        return aggregated

    def weighted_average(self, metrics: List[Tuple[int, dict]]) -> dict:
        total_samples = sum(n for n, _ in metrics)
        if total_samples == 0:
            return {}
        avg_metrics = {}
        for key in metrics[0][1]:
            weighted_sum = sum(n * m[key] for n, m in metrics)
            avg_metrics[key] = weighted_sum / total_samples
        return avg_metrics
