WEIGHTS = {
    'lstm': 0.40,
    'isolation_forest': 0.30,
    'autoencoder': 0.30,
}

THRESHOLD_LOW = 0.40
THRESHOLD_HIGH = 0.70

DECISION_NORMAL = "NORMAL"
DECISION_SUSPICIOUS = "SUSPICIOUS"
DECISION_THREAT_MEDIUM = "THREAT_MEDIUM"
DECISION_THREAT_HIGH = "THREAT_HIGH"


def fuse_scores(score_lstm: float, score_if: float, score_ae: float) -> float:
    score_final = (
        WEIGHTS['lstm'] * score_lstm +
        WEIGHTS['isolation_forest'] * score_if +
        WEIGHTS['autoencoder'] * score_ae
    )
    return round(float(score_final), 4)


def classify_decision(score_ensemble: float) -> str:
    if score_ensemble >= 0.85:
        return DECISION_THREAT_HIGH
    elif score_ensemble >= 0.70:
        return DECISION_THREAT_MEDIUM
    elif score_ensemble >= 0.40:
        return DECISION_SUSPICIOUS
    else:
        return DECISION_NORMAL


def requires_airo(decision: str) -> bool:
    return decision in (DECISION_THREAT_HIGH, DECISION_THREAT_MEDIUM)


def airo_delay_ms(decision: str) -> int:
    if decision == DECISION_THREAT_HIGH:
        return 0
    elif decision == DECISION_THREAT_MEDIUM:
        return 5000
    return -1
