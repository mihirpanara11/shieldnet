import numpy as np
from typing import Dict, List, Optional


class OnlineNormalizer:
    def __init__(self, n_features: int = 47):
        self.n_features = n_features
        self.count = 0
        self.mean = np.zeros(n_features, dtype=np.float64)
        self.M2 = np.zeros(n_features, dtype=np.float64)
        self.std = np.ones(n_features, dtype=np.float64)

    def update(self, features: np.ndarray):
        self.count += 1
        delta = features - self.mean
        self.mean += delta / self.count
        delta2 = features - self.mean
        self.M2 += delta * delta2
        if self.count > 1:
            self.std = np.sqrt(self.M2 / (self.count - 1))
            self.std = np.clip(self.std, 1e-8, None)

    def normalize(self, features: np.ndarray) -> np.ndarray:
        normalized = (features - self.mean) / self.std
        return np.clip(normalized, -5.0, 5.0)

    def get_params(self) -> dict:
        return {
            "mean": self.mean.tolist(),
            "std": self.std.tolist(),
            "count": self.count,
        }

    def load_params(self, mean: List[float], std: List[float], count: int):
        self.mean = np.array(mean, dtype=np.float64)
        self.std = np.array(std, dtype=np.float64)
        self.count = count


class WelfordNormalizer:
    def __init__(self, n_features: int = 47):
        self.n_features = n_features
        self.count = 0
        self.mean = np.zeros(n_features, dtype=np.float64)
        self.M2 = np.zeros(n_features, dtype=np.float64)
        self._min = np.full(n_features, np.inf)
        self._max = np.full(n_features, -np.inf)

    def update(self, x: np.ndarray):
        self.count += 1
        delta = x - self.mean
        self.mean += delta / self.count
        delta2 = x - self.mean
        self.M2 += delta * delta2
        np.minimum(self._min, x, out=self._min)
        np.maximum(self._max, x, out=self._max)

    def variance(self) -> np.ndarray:
        if self.count < 2:
            return np.ones(self.n_features)
        return self.M2 / (self.count - 1)

    def std(self) -> np.ndarray:
        return np.sqrt(np.clip(self.variance(), 1e-8, None))

    def zscore(self, x: np.ndarray) -> np.ndarray:
        return np.clip((x - self.mean) / self.std(), -5.0, 5.0)

    def minmax(self, x: np.ndarray) -> np.ndarray:
        rng = self._max - self._min
        rng = np.where(rng < 1e-8, 1.0, rng)
        return (x - self._min) / rng

    def get_state(self) -> dict:
        return {
            "count": self.count,
            "mean": self.mean.tolist(),
            "M2": self.M2.tolist(),
            "min": self._min.tolist(),
            "max": self._max.tolist(),
        }

    def reset(self):
        self.count = 0
        self.mean = np.zeros(self.n_features, dtype=np.float64)
        self.M2 = np.zeros(self.n_features, dtype=np.float64)
        self._min = np.full(self.n_features, np.inf)
        self._max = np.full(self.n_features, -np.inf)

    def set_state(self, state: dict):
        self.count = state["count"]
        self.mean = np.array(state["mean"], dtype=np.float64)
        self.M2 = np.array(state["M2"], dtype=np.float64)
        self._min = np.array(state["min"], dtype=np.float64)
        self._max = np.array(state["max"], dtype=np.float64)
