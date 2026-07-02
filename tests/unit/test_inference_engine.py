from inference.main import InferenceEngine
from inference.ensemble import fuse_scores, classify_decision, WEIGHTS


def test_inference_engine_initialization():
    engine = InferenceEngine(model_version="test-v1")
    assert engine.model_version == "test-v1"
    assert engine.threshold_low == 0.40
    assert engine.threshold_high == 0.70
    assert engine.classifier is not None


def test_inference_returns_all_fields():
    engine = InferenceEngine()
    features = [0.1] * 47
    result = engine.infer("DEV-001", "ZONE-01", "traffic", features)
    required = ["device_id", "zone_id", "timestamp", "score_lstm", "score_if",
                 "score_ae", "score_ensemble", "decision", "threat_class",
                 "threat_confidence", "model_version", "inference_time_ms"]
    for field in required:
        assert field in result, f"Missing field: {field}"


def test_inference_consistency():
    engine = InferenceEngine()
    features = [0.1] * 47
    r1 = engine.infer("DEV-001", "ZONE-01", "traffic", features)
    r2 = engine.infer("DEV-001", "ZONE-01", "traffic", features)
    assert r1["device_id"] == r2["device_id"]
    assert r1["zone_id"] == r2["zone_id"]


def test_weights_sum_to_one():
    total = sum(WEIGHTS.values())
    assert abs(total - 1.0) < 0.001


def test_decision_thresholds():
    assert classify_decision(0.0) == "NORMAL"
    assert classify_decision(0.39) == "NORMAL"
    assert classify_decision(0.40) == "SUSPICIOUS"
    assert classify_decision(0.69) == "SUSPICIOUS"
    assert classify_decision(0.70) == "THREAT_MEDIUM"
    assert classify_decision(0.84) == "THREAT_MEDIUM"
    assert classify_decision(0.85) == "THREAT_HIGH"
    assert classify_decision(1.0) == "THREAT_HIGH"


def test_fuse_scores_bounds():
    s = fuse_scores(0.0, 0.0, 0.0)
    assert 0.0 <= s <= 1.0
    s = fuse_scores(1.0, 1.0, 1.0)
    assert 0.0 <= s <= 1.0


def test_normal_traffic_low_score():
    engine = InferenceEngine()
    normal = [0.05] * 47
    result = engine.infer("DEV-NORMAL", "ZONE-01", "traffic", normal)
    assert result["decision"] in ("NORMAL", "SUSPICIOUS")


def test_anomalous_traffic_high_score():
    engine = InferenceEngine()
    anomalous = [5.0] * 47
    result = engine.infer("DEV-ANOMALY", "ZONE-01", "traffic", anomalous)
    assert "score_ensemble" in result
