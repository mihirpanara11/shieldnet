import numpy as np
from fl_client.dp_noise import apply_dp_noise, compute_gradient_delta
from fl_server.strategy import FedAvgStrategy
from fl_server.model_registry import ModelRegistry


def test_gradient_delta_shape():
    old = [np.array([1.0, 2.0, 3.0])]
    new = [np.array([1.5, 2.5, 3.5])]
    delta = compute_gradient_delta(new, old)
    assert len(delta) == 1
    assert delta[0].shape == (3,)


def test_gradient_delta_values():
    old = [np.array([1.0, 2.0, 3.0])]
    new = [np.array([1.5, 2.5, 3.5])]
    delta = compute_gradient_delta(new, old)
    np.testing.assert_array_almost_equal(delta[0], [0.5, 0.5, 0.5])


def test_dp_noise_adds_noise():
    grads = [np.zeros(10, dtype=np.float32)]
    noisy = apply_dp_noise(grads, num_samples=100)
    assert not np.array_equal(grads[0], noisy[0])


def test_dp_noise_preserves_shape():
    shapes = [(47,), (128,), (64, 32)]
    grads = [np.random.randn(*s).astype(np.float32) for s in shapes]
    noisy = apply_dp_noise(grads, num_samples=50)
    for orig, n in zip(grads, noisy):
        assert orig.shape == n.shape


def test_fedavg_requires_min_clients():
    strategy = FedAvgStrategy(min_clients=3)
    result = strategy.aggregate([])
    assert result is None


def test_fedavg_single_client():
    strategy = FedAvgStrategy(min_clients=1)
    grads = [([np.array([1.0, 2.0])], 10)]
    result = strategy.aggregate(grads)
    assert result is not None
    assert len(result) == 1


def test_fedavg_multiple_clients():
    strategy = FedAvgStrategy(min_clients=2)
    c1 = ([np.array([1.0, 2.0])], 10)
    c2 = ([np.array([3.0, 4.0])], 20)
    result = strategy.aggregate([c1, c2])
    assert result is not None
    expected = (1.0 * 10 + 3.0 * 20) / 30
    assert abs(result[0][0] - expected) < 0.01


def test_model_registry():
    reg = ModelRegistry()
    status = reg.get_status()
    assert status["current_round"] == 0
    assert "global-v" in status["global_model_version"]


def test_model_registry_round():
    reg = ModelRegistry()
    version = reg.register_round(1, "ZONE-01", {"loss": 0.1, "auc": 0.95, "samples": 100})
    assert version == "global-v1"
    status = reg.get_status()
    assert status["current_round"] == 1
    assert status["participating_zones"] == 1


def test_model_registry_privacy():
    reg = ModelRegistry()
    reg.consume_privacy_budget(1.0)
    reg.consume_privacy_budget(1.0)
    status = reg.get_status()
    assert status["privacy_epsilon_consumed"] == 2.0
