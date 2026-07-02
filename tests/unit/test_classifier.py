from inference.classifiers.threat_classifier import ThreatClassifier, THREAT_CLASSES, CLASS_IDS, THREAT_CLASSIFIER_INPUT_FEATURES
import numpy as np


def test_classifier_initialization():
    clf = ThreatClassifier()
    assert clf.model_path is None
    assert not clf.is_loaded


def test_classifier_predict_without_model():
    clf = ThreatClassifier()
    features = np.zeros(47, dtype=np.float32)
    threat, conf = clf.predict(features)
    assert threat == "Unknown"
    assert conf == 0.0


def test_threat_classes_complete():
    assert len(THREAT_CLASSES) == 7
    assert THREAT_CLASSES[0] == "DDoS"
    assert THREAT_CLASSES[1] == "Botnet"
    assert THREAT_CLASSES[2] == "Unauthorized"
    assert THREAT_CLASSES[3] == "MitM"
    assert THREAT_CLASSES[4] == "Ransomware"
    assert THREAT_CLASSES[5] == "Scanning"
    assert THREAT_CLASSES[6] == "Unknown"


def test_class_ids_reversible():
    for k, v in THREAT_CLASSES.items():
        assert CLASS_IDS[v] == k


def test_input_features_range():
    assert len(THREAT_CLASSIFIER_INPUT_FEATURES) == 29
    for idx in THREAT_CLASSIFIER_INPUT_FEATURES:
        assert 0 <= idx < 47


def test_classifier_train_and_predict():
    clf = ThreatClassifier()
    n_samples = 200
    X = np.random.randn(n_samples, 29).astype(np.float32)
    y = np.random.randint(0, 7, size=n_samples)

    clf.train(X, y)
    assert clf.is_loaded

    test_features = np.zeros(47, dtype=np.float32)
    threat, conf = clf.predict(test_features)
    assert threat in THREAT_CLASSES.values()
    assert 0.0 <= conf <= 1.0
