import numpy as np
import pytest
from features.extractors.base import FeatureExtractor, DeviceBaseline
from features.normalization import OnlineNormalizer, WelfordNormalizer
from features.device_baseline import DeviceIDAnonymizer
from inference.ensemble import fuse_scores, classify_decision
from fl_client.dp_noise import apply_dp_noise, compute_gradient_delta
from fl_server.strategy import FedAvgStrategy
from airo.state_machine import StateMachine, IncidentReport


def make_baseline():
    return DeviceBaseline(
        device_id="TRF-0000", category="traffic", protocol="MQTT",
        msg_rate_mean=10.0, msg_rate_std=2.0,
        payload_size_mean=256.0, payload_size_std=32.0,
        known_dest_ips={"hash123"}, known_dest_ports={8883},
        active_hours=set(range(8, 18)),
        baseline_age_days=14.0, firmware_age_days=30.0,
    )


# === Feature Extractor Edge Cases ===

def test_extractor_empty_payload():
    extractor = FeatureExtractor("TRF-0000", make_baseline())
    features = extractor.extract({"protocol": "MQTT", "payload_sample": b""}, now=1000.0)
    assert len(features) == 47
    assert features[5] == 0.0
    assert features[9] == 0.0


def test_extractor_no_keys():
    extractor = FeatureExtractor("TRF-0000", make_baseline())
    features = extractor.extract({}, now=1000.0)
    assert len(features) == 47
    assert features[5] == 0.0  # payload_size defaults to 0


def test_extractor_rapid_messages():
    baseline = make_baseline()
    extractor = FeatureExtractor("TRF-0000", baseline)
    for i in range(100):
        features = extractor.extract({"payload_size": 256, "protocol": "MQTT",
                                      "dest_ip_hash": "hash123", "dest_port": 8883,
                                      "payload_sample": b"x", "device_uptime_hours": 100.0},
                                     now=1000.0 + i * 0.001)
    assert features[0] >= 1.0
    assert features[46] >= 0.0


def test_extractor_large_payload():
    extractor = FeatureExtractor("TRF-0000", make_baseline())
    large = bytes([i % 256 for i in range(256)] * 256)  # all byte values
    features = extractor.extract({"protocol": "MQTT", "payload_size": 65536,
                                   "payload_sample": large}, now=1000.0)
    assert features[9] > 0.0


def test_normalizer_single_value():
    norm = WelfordNormalizer(3)
    norm.update(np.array([5.0, 5.0, 5.0], dtype=np.float64))
    assert norm.count == 1
    var = norm.variance()
    assert np.all(var == 1.0)


def test_normalizer_zscore_single():
    norm = WelfordNormalizer(3)
    norm.update(np.array([10.0, 10.0, 10.0], dtype=np.float64))
    z = norm.zscore(np.array([10.0, 10.0, 10.0], dtype=np.float64))
    assert np.all(z == 0.0)


def test_normalizer_reset():
    norm = WelfordNormalizer(3)
    for _ in range(10):
        norm.update(np.array([1.0, 2.0, 3.0], dtype=np.float64))
    norm.reset()
    assert norm.count == 0
    assert np.all(norm.mean == 0.0)


# === Device Anonymizer Edge Cases ===

def test_anonymizer_empty_mac():
    anon = DeviceIDAnonymizer(zone_salt="test")
    device_id = anon.anonymize("")
    assert device_id.startswith("DEV-")


def test_anonymizer_invalid_mac():
    anon = DeviceIDAnonymizer(zone_salt="test")
    device_id = anon.anonymize("not-a-mac-address")
    assert device_id.startswith("DEV-")
    assert len(device_id) == 12


# === Ensemble Edge Cases ===

def test_fuse_scores_extremes():
    assert fuse_scores(0.0, 0.0, 0.0) == 0.0
    s = fuse_scores(1.0, 1.0, 1.0)
    assert 0.0 <= s <= 1.0


def test_classify_decision_boundaries():
    assert classify_decision(-0.01) == "NORMAL"
    assert classify_decision(0.3999) == "NORMAL"
    assert classify_decision(0.40) == "SUSPICIOUS"
    assert classify_decision(0.6999) == "SUSPICIOUS"
    assert classify_decision(0.70) == "THREAT_MEDIUM"
    assert classify_decision(0.8499) == "THREAT_MEDIUM"
    assert classify_decision(0.85) == "THREAT_HIGH"
    assert classify_decision(1.5) == "THREAT_HIGH"


# === DP Noise Edge Cases ===

def test_dp_noise_no_samples():
    grads = [np.array([1.0, 2.0, 3.0], dtype=np.float32)]
    noisy = apply_dp_noise(grads, num_samples=0)
    np.testing.assert_array_almost_equal(grads[0], noisy[0])


def test_dp_noise_zero_grads():
    grads = [np.zeros(5, dtype=np.float32)]
    noisy = apply_dp_noise(grads, num_samples=100)
    assert not np.allclose(grads[0], noisy[0])


def test_dp_noise_empty_list():
    result = apply_dp_noise([], num_samples=10)
    assert result == []


def test_gradient_delta_empty():
    delta = compute_gradient_delta([], [])
    assert delta == []


def test_gradient_delta_mismatch():
    old = [np.array([1.0, 2.0])]
    new = [np.array([1.0, 2.0, 3.0])]
    with pytest.raises(ValueError):
        compute_gradient_delta(new, old)


# === FL Strategy Edge Cases ===

def test_fedavg_insufficient_clients():
    strategy = FedAvgStrategy(min_clients=5)
    assert strategy.aggregate([([np.array([1.0])], 10)]) is None


def test_fedavg_zero_weights():
    strategy = FedAvgStrategy(min_clients=1)
    result = strategy.aggregate([([np.array([0.0, 0.0])], 0)])
    if result is not None:
        assert np.all(np.isfinite(result[0]))


# === AIRO State Machine Edge Cases ===

def test_state_machine_double_start():
    sm = StateMachine()
    sm.start()
    sm.start()
    assert sm.state == "QUEUED"


def test_state_machine_cancel_before_execute():
    sm = StateMachine(confirmation_delay_ms=100)
    sm.start()
    sm.cancel()
    assert sm.wait_for_confirmation() is False


def test_state_machine_elapsed_zero():
    sm = StateMachine()
    assert sm.elapsed_ms == 0


# === Incident Report Edge Cases ===

def test_incident_report_empty_device_id():
    inc = IncidentReport(
        zone_id="ZONE-00", device_category="unknown",
        threat_class="Unknown", confidence_score=0.0,
        individual_scores={}, playbook_executed="", actions_taken=[],
        containment_time_ms=0,
    )
    assert inc.device_id == ""
    d = inc.to_dict()
    assert d["device_id"] == ""
    assert d["timestamp"] != ""


def test_incident_report_with_device_id():
    inc = IncidentReport(
        zone_id="ZONE-04", device_category="traffic",
        threat_class="DDoS", confidence_score=0.95,
        individual_scores={"lstm": 0.9, "if": 0.8, "ae": 0.7},
        playbook_executed="DDoS_RESPONSE_v2",
        actions_taken=["rate_limit"], containment_time_ms=1500,
        device_id="TRF-0042",
    )
    assert inc.device_id == "TRF-0042"
    assert inc.playbook == "DDoS_RESPONSE_v2"
    assert inc.actions == ["rate_limit"]
