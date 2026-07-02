from features.extractors.base import FeatureExtractor, DeviceBaseline


def make_baseline():
    return DeviceBaseline(
        device_id="TRF-0042",
        category="traffic",
        protocol="MQTT",
        msg_rate_mean=10.0,
        msg_rate_std=2.0,
        payload_size_mean=256.0,
        payload_size_std=32.0,
        known_dest_ips={"hash123"},
        known_dest_ports={8883},
        active_hours={8, 9, 10, 11, 12, 13, 14, 15, 16, 17},
        baseline_age_days=14.0,
        firmware_age_days=30.0,
    )


def test_feature_extraction_length():
    baseline = make_baseline()
    extractor = FeatureExtractor("TRF-0042", baseline)

    msg = {
        "payload_size": 256,
        "protocol": "MQTT",
        "qos": 1,
        "retain": False,
        "topic": "city/ZONE-04/traffic/TRF-0042/telemetry",
        "topic_pattern": "city/ZONE-04/traffic/TRF-0042/telemetry",
        "dest_ip_hash": "hash123",
        "dest_ip_is_external": False,
        "dest_ip_new_in_24h": False,
        "dest_port": 8883,
        "payload_sample": b"test data",
        "device_uptime_hours": 100.0,
        "zone_alert_level": 0,
    }

    features = extractor.extract(msg, now=1000.0)
    assert len(features) == 47, f"Expected 47 features, got {len(features)}"


def test_feature_extraction_values():
    baseline = make_baseline()
    extractor = FeatureExtractor("TRF-0042", baseline)
    msg = {
        "payload_size": 512,
        "protocol": "MQTT",
        "qos": 1,
        "retain": False,
        "topic": "city/ZONE-04/traffic/TRF-0042/telemetry",
        "topic_pattern": "city/ZONE-04/traffic/TRF-0042/telemetry",
        "dest_ip_hash": "hash123",
        "dest_ip_is_external": False,
        "dest_ip_new_in_24h": False,
        "dest_port": 8883,
        "payload_sample": b"test data",
        "device_uptime_hours": 100.0,
        "zone_alert_level": 0,
    }
    features = extractor.extract(msg, now=1000.0)
    assert features[5] == 512.0
    assert features[12] == 1.0
    assert features[18] == 1.0


def test_feature_extraction_multiple_messages():
    baseline = make_baseline()
    extractor = FeatureExtractor("TRF-0042", baseline)
    for i in range(5):
        msg = {"payload_size": 256, "protocol": "MQTT", "qos": 1, "retain": False,
               "topic": "city/ZONE-04/traffic/TRF-0042/telemetry",
               "topic_pattern": "test", "dest_ip_hash": "hash123",
               "dest_ip_is_external": False, "dest_ip_new_in_24h": False,
               "dest_port": 8883, "payload_sample": b"x"}
        extractor.extract(msg, now=1000.0 + i)

    msg = {"payload_size": 256, "protocol": "MQTT", "qos": 1, "retain": False,
           "topic": "city/ZONE-04/traffic/TRF-0042/telemetry",
           "topic_pattern": "test", "dest_ip_hash": "hash123",
           "dest_ip_is_external": False, "dest_ip_new_in_24h": False,
           "dest_port": 8883, "payload_sample": b"x"}
    features = extractor.extract(msg, now=1005.0)
    assert features[0] >= 5.0
