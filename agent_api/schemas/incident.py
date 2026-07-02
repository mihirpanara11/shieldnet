from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime


class IndividualScores(BaseModel):
    lstm: float = 0.0
    isolation_forest: float = 0.0
    autoencoder: float = 0.0


class IncidentReport(BaseModel):
    incident_id: str
    timestamp_detected: str
    timestamp_contained: str = ""
    containment_time_ms: int = 0
    zone_id: str
    device_category: str
    threat_class: str
    confidence_score: float
    individual_scores: IndividualScores
    playbook_executed: str = ""
    actions_taken: List[str] = []
    status: str = "ACTIVE"
    false_positive_confirmed: bool = False
    operator_review_required: bool = False
    auto_restored: bool = False
    notes: str = ""


class ThreatReviewRequest(BaseModel):
    action: str
    operator_id: str
    notes: str = ""


class OverrideCommand(BaseModel):
    device_id: str
    zone_id: str
    action: str
    duration_sec: int = 3600
    reason: str = ""
    operator_id: str = ""
