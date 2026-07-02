from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class IncidentBase(BaseModel):
    incident_ref: str
    zone_id: str
    device_category: str
    threat_class: str
    confidence_score: float
    status: str = "ACTIVE"


class IncidentCreate(IncidentBase):
    detected_at: datetime = datetime.now()
    score_lstm: Optional[float] = None
    score_isolation_forest: Optional[float] = None
    score_autoencoder: Optional[float] = None
    playbook_id: Optional[str] = None
    actions_taken: Optional[list] = None


class IncidentResponse(IncidentBase):
    id: str
    detected_at: datetime
    contained_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    containment_time_ms: Optional[int] = None
    false_positive: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DeviceProfileBase(BaseModel):
    device_id: str
    zone_id: str
    category: str
    protocol: str


class DeviceProfileCreate(DeviceProfileBase):
    pass


class DeviceProfileResponse(DeviceProfileBase):
    id: str
    baseline_established: bool = False
    is_quarantined: bool = False
    alert_count_total: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class FLStatusResponse(BaseModel):
    current_round: int
    global_model_version: str
    last_aggregation: str
    next_aggregation: str
    participating_zones: int
    global_auc_roc: float
    global_f1: float
    privacy_epsilon_consumed: float
    privacy_epsilon_budget: float
