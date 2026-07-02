import numpy as np
from features.normalization import OnlineNormalizer, WelfordNormalizer


def test_online_normalizer():
    norm = OnlineNormalizer(47)
    assert norm.n_features == 47
    assert norm.count == 0


def test_online_normalizer_update():
    norm = OnlineNormalizer(3)
    features = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    norm.update(features)
    assert norm.count == 1
    np.testing.assert_array_almost_equal(norm.mean, features)


def test_online_normalizer_normalize():
    norm = OnlineNormalizer(3)
    for _ in range(100):
        norm.update(np.array([1.0, 2.0, 3.0], dtype=np.float64))
    result = norm.normalize(np.array([1.0, 2.0, 3.0], dtype=np.float64))
    assert result.shape == (3,)
    assert np.all(np.isfinite(result))


def test_welford_normalizer():
    norm = WelfordNormalizer(5)
    assert norm.n_features == 5
    assert norm.count == 0


def test_welford_update():
    norm = WelfordNormalizer(3)
    for i in range(10):
        norm.update(np.array([float(i), float(i * 2), float(i * 3)], dtype=np.float64))
    assert norm.count == 10
    var = norm.variance()
    assert var.shape == (3,)
    assert np.all(var >= 0)


def test_welford_zscore():
    norm = WelfordNormalizer(3)
    for i in range(50):
        norm.update(np.array([1.0, 2.0, 3.0], dtype=np.float64))
    z = norm.zscore(np.array([1.5, 2.5, 3.5], dtype=np.float64))
    assert z.shape == (3,)
    assert np.all(np.isfinite(z))
    assert np.all(z >= -5.0)
    assert np.all(z <= 5.0)


def test_welford_get_set_state():
    norm = WelfordNormalizer(3)
    for i in range(10):
        norm.update(np.array([float(i), float(i), float(i)], dtype=np.float64))
    state = norm.get_state()
    assert state["count"] == 10

    norm2 = WelfordNormalizer(3)
    norm2.set_state(state)
    assert norm2.count == 10
    np.testing.assert_array_almost_equal(norm.mean, norm2.mean)
