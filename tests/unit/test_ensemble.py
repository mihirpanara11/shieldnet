from inference.ensemble import fuse_scores, classify_decision, DECISION_NORMAL, DECISION_SUSPICIOUS, DECISION_THREAT_MEDIUM, DECISION_THREAT_HIGH


def test_fuse_scores_normal():
    score = fuse_scores(0.1, 0.1, 0.1)
    expected = 0.4 * 0.1 + 0.3 * 0.1 + 0.3 * 0.1
    assert score == round(expected, 4)
    assert classify_decision(score) == DECISION_NORMAL


def test_fuse_scores_suspicious():
    score = fuse_scores(0.5, 0.5, 0.5)
    assert 0.40 <= score <= 0.70
    assert classify_decision(score) == DECISION_SUSPICIOUS


def test_fuse_scores_threat_medium():
    score = fuse_scores(0.8, 0.7, 0.7)
    assert 0.70 <= score <= 0.85
    assert classify_decision(score) == DECISION_THREAT_MEDIUM


def test_fuse_scores_threat_high():
    score = fuse_scores(0.95, 0.90, 0.90)
    assert score >= 0.85
    assert classify_decision(score) == DECISION_THREAT_HIGH


def test_classify_boundary():
    assert classify_decision(0.39) == DECISION_NORMAL
    assert classify_decision(0.40) == DECISION_SUSPICIOUS
    assert classify_decision(0.69) == DECISION_SUSPICIOUS
    assert classify_decision(0.70) == DECISION_THREAT_MEDIUM
    assert classify_decision(0.84) == DECISION_THREAT_MEDIUM
    assert classify_decision(0.85) == DECISION_THREAT_HIGH


def test_weights_sum():
    from inference.ensemble import WEIGHTS
    total = sum(WEIGHTS.values())
    assert abs(total - 1.0) < 0.001
