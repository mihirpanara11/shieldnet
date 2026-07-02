from features.device_baseline import DeviceBaselineProfile, DeviceIDAnonymizer, BaselineBuilder


def test_device_anonymizer():
    anon = DeviceIDAnonymizer(zone_salt="test-salt")
    device_id = anon.anonymize("AA:BB:CC:DD:EE:FF")
    assert device_id.startswith("DEV-")
    assert len(device_id) == 12


def test_anonymizer_deterministic():
    anon = DeviceIDAnonymizer(zone_salt="test-salt")
    id1 = anon.anonymize("AA:BB:CC:DD:EE:FF")
    id2 = anon.anonymize("AA:BB:CC:DD:EE:FF")
    assert id1 == id2


def test_anonymizer_different_macs():
    anon = DeviceIDAnonymizer(zone_salt="test-salt")
    id1 = anon.anonymize("AA:BB:CC:DD:EE:FF")
    id2 = anon.anonymize("11:22:33:44:55:66")
    assert id1 != id2


def test_category_prefix():
    anon = DeviceIDAnonymizer()
    assert anon.anonymize_category("traffic", 42) == "TRF-0042"
    assert anon.anonymize_category("camera", 1) == "CAM-0001"
    assert anon.anonymize_category("energy", 100) == "ENR-0100"
    assert anon.anonymize_category("other", 9999) == "OTH-9999"


def test_baseline_builder():
    builder = BaselineBuilder("DEV-TEST", "traffic", "MQTT")
    assert not builder.is_ready()
    assert builder.elapsed_hours() < 1.0


def test_baseline_builder_record():
    builder = BaselineBuilder("DEV-TEST", "traffic", "MQTT")
    for _ in range(10):
        builder.record_message({
            "payload_size": 256,
            "dest_ip_hash": "hash123",
            "dest_port": 8883,
        })
    profile = builder.build()
    assert profile.payload_size_mean == 256.0
    assert "hash123" in profile.known_dest_ips
    assert 8883 in profile.known_dest_ports


def test_device_profile_properties():
    import time
    profile = DeviceBaselineProfile(
        device_id="DEV-001", zone_id="ZONE-01", category="traffic",
        protocol="MQTT", expected_topic_prefix="city/ZONE-01/traffic/",
        expected_update_hz=10.0, firmware_version="1.0",
        baseline_created_at=time.time() - 86400 * 14,
        firmware_updated_at=time.time() - 86400 * 30,
        enrollment_time=time.time() - 86400 * 20,
    )
    assert abs(profile.baseline_age_days - 14.0) < 1.0
    assert abs(profile.firmware_age_days - 30.0) < 1.0
    assert abs(profile.uptime_hours - 480.0) < 24.0
