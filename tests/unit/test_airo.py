from airo.state_machine import StateMachine, IncidentReport
from airo.playbooks.ddos_playbook import DDoSPlaybook
from airo.playbooks.botnet_playbook import BotnetPlaybook


def test_state_machine_normal_flow():
    sm = StateMachine(confirmation_delay_ms=0)
    assert sm.state == "IDLE"
    sm.start()
    assert sm.state == "QUEUED"
    sm.execute()
    assert sm.state == "EXECUTING"
    sm.complete()
    assert sm.state == "COMPLETE"


def test_state_machine_cancel():
    sm = StateMachine(confirmation_delay_ms=5000)
    sm.start()
    sm.cancel()
    assert sm.state == "CANCELLED"
    assert sm.should_cancel


def test_state_machine_no_delay():
    sm = StateMachine(confirmation_delay_ms=0)
    sm.start()
    assert sm.wait_for_confirmation() is True


def test_incident_report_creation():
    incident = IncidentReport(
        zone_id="ZONE-04",
        device_category="traffic_sensor",
        threat_class="DDoS",
        confidence_score=0.923,
        individual_scores={"lstm": 0.94, "isolation_forest": 0.88, "autoencoder": 0.91},
        playbook_executed="DDoS_RESPONSE_v2",
        actions_taken=["rate_limit_mac", "quarantine_vlan"],
        containment_time_ms=1459,
        device_id="TRF-0042",
    )
    assert incident.incident_id.startswith("INC-")
    assert incident.threat_class == "DDoS"
    assert incident.status == "CONTAINED"
    assert incident.device_id == "TRF-0042"
    assert incident.timestamp != ""
    assert incident.playbook == "DDoS_RESPONSE_v2"
    assert incident.actions == ["rate_limit_mac", "quarantine_vlan"]

    d = incident.to_dict()
    assert d["device_id"] == "TRF-0042"
    assert d["timestamp"] != ""
    assert d["playbook"] == "DDoS_RESPONSE_v2"
    assert d["actions"] == ["rate_limit_mac", "quarantine_vlan"]


def test_ddos_playbook():
    playbook = DDoSPlaybook()
    result = playbook.execute()
    assert result["playbook_id"] == "DDoS_RESPONSE_v2"
    assert len(result["actions_taken"]) > 0
    assert result["status"] == "COMPLETE"


def test_botnet_playbook():
    playbook = BotnetPlaybook()
    result = playbook.execute()
    assert result["playbook_id"] == "BOTNET_RESPONSE_v1"
    assert len(result["actions_taken"]) > 0
