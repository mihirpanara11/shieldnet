import time
import uuid
import threading
import logging

logger = logging.getLogger("shieldnet.airo")


class AIROResponse:
    def __init__(self, incident_id: str, playbook: str,
                 actions: list, status: str,
                 containment_time_ms: int, error_message: str = ""):
        self.incident_id = incident_id
        self.playbook = playbook
        self.actions = actions
        self.status = status
        self.containment_time_ms = containment_time_ms
        self.error_message = error_message
        self.playbook_executed = playbook
        self.actions_taken = actions

    def to_dict(self) -> dict:
        return {
            "incident_id": self.incident_id,
            "playbook": self.playbook,
            "actions": self.actions,
            "status": self.status,
            "containment_time_ms": self.containment_time_ms,
            "error_message": self.error_message,
        }


class StateMachine:
    IDLE = "IDLE"
    QUEUED = "QUEUED"
    EXECUTING = "EXECUTING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

    def __init__(self, confirmation_delay_ms: int = 5000):
        self.state = self.IDLE
        self.confirmation_delay_ms = confirmation_delay_ms
        self._cancel_flag = False
        self._lock = threading.Lock()
        self._start_time: float = 0.0

    def start(self):
        with self._lock:
            self.state = self.QUEUED
            self._start_time = time.time()
            self._cancel_flag = False

    def execute(self):
        with self._lock:
            self.state = self.EXECUTING

    def complete(self):
        with self._lock:
            self.state = self.COMPLETE

    def fail(self):
        with self._lock:
            self.state = self.FAILED

    def cancel(self):
        with self._lock:
            self.state = self.CANCELLED
            self._cancel_flag = True

    @property
    def should_cancel(self) -> bool:
        return self._cancel_flag

    @property
    def elapsed_ms(self) -> int:
        return int((time.time() - self._start_time) * 1000) if self._start_time > 0 else 0

    def wait_for_confirmation(self) -> bool:
        if self.confirmation_delay_ms <= 0:
            return True
        poll_interval = 0.1
        waited = 0
        while waited < self.confirmation_delay_ms:
            if self._cancel_flag:
                return False
            time.sleep(poll_interval)
            waited += int(poll_interval * 1000)
        return not self._cancel_flag


class IncidentReport:
    def __init__(self, zone_id: str, device_category: str, threat_class: str,
                 confidence_score: float, individual_scores: dict,
                 playbook_executed: str, actions_taken: list,
                 containment_time_ms: int, device_id: str = "",
                 timestamp: str = ""):
        self.incident_id = f"INC-2025-{uuid.uuid4().hex[:8]}"
        now_str = time.strftime("%Y-%m-%dT%H:%M:%S.") + f"{int(time.time()*1000)%1000:03d}Z"
        self.timestamp = timestamp or now_str
        self.timestamp_detected = now_str
        self.timestamp_contained = ""
        self.containment_time_ms = containment_time_ms
        self.zone_id = zone_id
        self.device_id = device_id
        self.device_category = device_category
        self.threat_class = threat_class
        self.confidence_score = confidence_score
        self.individual_scores = individual_scores
        self.playbook = playbook_executed
        self.actions = actions_taken
        self.playbook_executed = playbook_executed
        self.actions_taken = actions_taken
        self.status = "CONTAINED"
        self.false_positive_confirmed = False
        self.operator_review_required = False
        self.auto_restored = False
        self.notes = ""

    def to_dict(self) -> dict:
        self.timestamp_contained = time.strftime("%Y-%m-%dT%H:%M:%S.") + f"{int(time.time()*1000)%1000:03d}Z"
        return {
            "incident_id": self.incident_id,
            "timestamp": self.timestamp,
            "timestamp_detected": self.timestamp_detected,
            "timestamp_contained": self.timestamp_contained,
            "containment_time_ms": self.containment_time_ms,
            "zone_id": self.zone_id,
            "device_id": self.device_id,
            "device_category": self.device_category,
            "threat_class": self.threat_class,
            "confidence_score": self.confidence_score,
            "individual_scores": self.individual_scores,
            "playbook": self.playbook,
            "actions": self.actions,
            "playbook_executed": self.playbook_executed,
            "actions_taken": self.actions_taken,
            "status": self.status,
            "false_positive_confirmed": self.false_positive_confirmed,
            "operator_review_required": self.operator_review_required,
            "auto_restored": self.auto_restored,
            "notes": self.notes,
        }
