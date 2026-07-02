import numpy as np
from fl_client.dp_noise import apply_dp_noise, compute_gradient_delta


def test_apply_dp_noise():
    gradients = [np.array([1.0, 2.0, 3.0], dtype=np.float32)]
    noisy = apply_dp_noise(gradients, num_samples=100)
    assert len(noisy) == 1
    assert noisy[0].shape == (3,)


def test_compute_gradient_delta():
    weights_new = [np.array([1.5, 2.5, 3.5], dtype=np.float32)]
    weights_global = [np.array([1.0, 2.0, 3.0], dtype=np.float32)]
    delta = compute_gradient_delta(weights_new, weights_global)
    assert len(delta) == 1
    np.testing.assert_array_almost_equal(delta[0], [0.5, 0.5, 0.5])


def test_dp_noise_clipping():
    large_grad = [np.array([100.0, 0.0, 0.0], dtype=np.float32)]
    noisy = apply_dp_noise(large_grad, num_samples=10)
    assert len(noisy) == 1
    assert np.isfinite(noisy[0]).all()


def test_dp_noise_shape_preserved():
    shapes = [(47,), (128, 47), (64,)]
    grads = [np.random.randn(*s).astype(np.float32) for s in shapes]
    noisy = apply_dp_noise(grads, num_samples=50)
    for orig, noised in zip(grads, noisy):
        assert orig.shape == noised.shape
