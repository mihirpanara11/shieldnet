import time
import logging
from typing import Optional, Callable

from airo.state_machine import StateMachine, AIROResponse, IncidentReport
from airo.playbooks.ddos_playbook import DDoSPlaybook
from airo.playbooks.botnet_playbook import BotnetPlaybook
from airo.playbooks.unauthorized_playbook import UnauthorizedPlaybook
from airo.playbooks.mitm_playbook import MitMPlaybook
from airo.playbooks.ransomware_playbook import RansomwarePlaybook
from airo.actions.network_actions import NetworkAction
from airo.actions.mqtt_actions import MQTTAction
from airo.actions.notification_actions import NotificationAction
from airo.incident_reporter import IncidentReporter

logger = logging.getLogger("shieldnet.airo.engine")

PLAYBOOK_MAP = {
    "DDoS": DDoSPlaybook,
    "Botnet": BotnetPlaybook,
    "Unauthorized": UnauthorizedPlaybook,
    "MitM": MitMPlaybook,
    "Ransomware": RansomwarePlaybook,
}


class AIROEngine:
    def __init__(self, mqtt_broker: str = "mosquitto:1883",
                 soc_webhook: str = "",
                 confirmation_delay_ms: int = 5000):
        self.confirmation_delay_ms = confirmation_delay_ms
        self.network = NetworkAction()
        self.mqtt = MQTTAction()
        self.notifications = NotificationAction(soc_webhook)
        self.reporter = IncidentReporter()
        self._state_machines: dict = {}
        self._on_threat_callbacks: list = []

    def on_threat(self, callback: Callable):
        self._on_threat_callbacks.append(callback)

    def _notify_threat(self, incident: dict):
        for cb in self._on_threat_callbacks:
            try:
                cb(incident)
            except Exception:
                pass

    def handle_threat(self, threat_event: dict) -> AIROResponse:
        incident_id = threat_event.get("incident_id", f"INC-2025-{int(time.time())}")
        threat_class = threat_event.get("threat_class", "Unknown")
        confidence = threat_event.get("confidence_score", 0.0)
        decision = threat_event.get("decision", "THREAT_MEDIUM")
        score_lstm = threat_event.get("score_lstm", 0.0)
        score_if = threat_event.get("score_if", 0.0)
        score_ae = threat_event.get("score_ae", 0.0)

        sm = StateMachine(self.confirmation_delay_ms)
        self._state_machines[incident_id] = sm
        sm.start()

        if decision == "THREAT_HIGH":
            proceed = True
        elif decision == "THREAT_MEDIUM":
            proceed = sm.wait_for_confirmation()
        else:
            proceed = False

        if not proceed:
            sm.cancel()
            return AIROResponse(incident_id, "", [], "CANCELLED", 0)

        sm.execute()
        playbook_cls = PLAYBOOK_MAP.get(threat_class)
        if playbook_cls is None:
            sm.fail()
            return AIROResponse(incident_id, "", [], "FAILED", 0,
                                f"No playbook for {threat_class}")

        playbook = playbook_cls()
        result = playbook.execute()
        containment_ms = result.get("containment_time_ms", 0)
        actions_taken = result.get("actions_taken", [])

        individual_scores = {
            "lstm": score_lstm,
            "isolation_forest": score_if,
            "autoencoder": score_ae,
        }

        incident = IncidentReport(
            zone_id=threat_event.get("zone_id", ""),
            device_category=threat_event.get("device_category", ""),
            threat_class=threat_class,
            confidence_score=confidence,
            individual_scores=individual_scores,
            playbook_executed=playbook.playbook_id,
            actions_taken=actions_taken,
            containment_time_ms=containment_ms,
        )

        incident_dict = incident.to_dict()
        self.reporter.record_incident(incident_dict)
        self._notify_threat(incident_dict)

        sm.complete()
        return AIROResponse(
            incident_id=incident.incident_id,
            playbook=playbook.playbook_id,
            actions=actions_taken,
            status="COMPLETE",
            containment_time_ms=containment_ms,
        )

    def manual_override(self, override: dict) -> AIROResponse:
        action = override.get("action", "")
        device_id = override.get("device_id", "")
        duration_sec = override.get("duration_sec", 3600)

        actions_taken = []
        if action == "QUARANTINE":
            self.network.quarantine_device(device_id)
            actions_taken.append("quarantine_vlan")
        elif action == "RELEASE":
            self.network.restore_device(device_id)
            actions_taken.append("restore_device")
        elif action == "RATE_LIMIT":
            self.network.rate_limit_mac(device_id)
            actions_taken.append("rate_limit_mac")
        elif action == "FORCE_REAUTH":
            self.mqtt.revoke_tokens(device_id)
            actions_taken.append("force_reauth")
        elif action == "SANDBOX":
            self.network.sandbox_device(device_id)
            actions_taken.append("sandbox_vlan")

        return AIROResponse(
            incident_id=f"CMD-2025-{int(time.time())}",
            playbook="MANUAL_OVERRIDE",
            actions=actions_taken,
            status="EXECUTING",
            containment_time_ms=250,
        )

    def cancel_action(self, incident_id: str) -> AIROResponse:
        sm = self._state_machines.get(incident_id)
        if sm:
            sm.cancel()
        return AIROResponse(incident_id, "", [], "CANCELLED", 0)
