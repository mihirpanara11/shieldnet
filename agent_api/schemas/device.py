from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DeviceInfo(BaseModel):
    device_id: str
    category: str
    zone_id: str
    status: str = "NORMAL"
    last_seen: str = ""
    anomaly_score_current: float = 0.0
    baseline_established: bool = False
    baseline_age_days: float = 0.0


class DeviceEnrollRequest(BaseModel):
    device_mac: str
    zone_id: str
    category: str
    protocol: str = "MQTT"
    expected_topic_prefix: str = ""
    expected_update_hz: float = 1.0
    firmware_version: str = "0.0.0"
    notes: str = ""
