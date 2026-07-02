import numpy as np
from typing import List

EPSILON = 1.0
DELTA = 1e-5
CLIP_NORM = 1.0


def apply_dp_noise(gradients: List[np.ndarray], num_samples: int) -> List[np.ndarray]:
    if num_samples == 0 or not gradients:
        return [g.copy() for g in gradients]

    clipped = []
    for g in gradients:
        norm = np.linalg.norm(g)
        scale = max(1.0, norm / CLIP_NORM)
        clipped.append(g / scale)

    sensitivity = CLIP_NORM / num_samples
    sigma = sensitivity * np.sqrt(2 * np.log(1.25 / DELTA)) / max(EPSILON, 1e-8)

    noisy = [g + np.random.normal(0, sigma, g.shape) for g in clipped]
    return noisy


def compute_gradient_delta(weights_new: List[np.ndarray],
                           weights_global: List[np.ndarray]) -> List[np.ndarray]:
    return [wn - wg for wn, wg in zip(weights_new, weights_global)]
