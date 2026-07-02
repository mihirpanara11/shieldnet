import sys
sys.path.insert(0, '.')

from inference.main import InferenceEngine
from inference.ensemble import fuse_scores, classify_decision
import numpy as np


def test_inference_pipeline():
    engine = InferenceEngine(model_version="test-v1")
    features = [0.5] * 47
    result = engine.infer(
        device_id="TRF-0042",
        zone_id="ZONE-04",
        category="traffic",
        feature_vector=features,
    )
    assert result["device_id"] == "TRF-0042"
    assert result["zone_id"] == "ZONE-04"
    assert "score_lstm" in result
    assert "score_ensemble" in result
    assert "decision" in result
    assert result["inference_time_ms"] >= 0


def test_pipeline_end_to_end():
    engine = InferenceEngine(model_version="test-v1")

    normal_features = [0.1] * 47
    result_normal = engine.infer("DEV-001", "ZONE-01", "traffic", normal_features)
    assert result_normal["decision"] in ("NORMAL", "SUSPICIOUS")

    attack_features = [2.0] * 47
    result_attack = engine.infer("DEV-002", "ZONE-02", "camera", attack_features)
    assert "score_ensemble" in result_attack


def test_ensemble_scoring():
    normal_score = fuse_scores(0.1, 0.1, 0.1)
    assert classify_decision(normal_score) == "NORMAL"
    assert normal_score < 0.40

    high_score = fuse_scores(0.9, 0.9, 0.9)
    assert classify_decision(high_score) in ("THREAT_MEDIUM", "THREAT_HIGH")


def test_batch_inference():
    engine = InferenceEngine(model_version="test-v1")

    results = []
    for i in range(5):
        features = [float(i) / 10.0] * 47
        result = engine.infer(f"DEV-{i:04d}", "ZONE-04", "traffic", features)
        results.append(result)

    assert len(results) == 5
    for r in results:
        assert "score_ensemble" in r
        assert "decision" in r
