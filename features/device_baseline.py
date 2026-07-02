from dataclasses import dataclass, field
from typing import Set, Optional
import time
import hashlib
import hmac


@dataclass
class DeviceBaselineProfile:
    device_id: str
    zone_id: str
    category: str
    protocol: str
    expected_topic_prefix: str
    expected_update_hz: float
    firmware_version: str
    msg_rate_mean: float = 0.0
    msg_rate_std: float = 0.0
    payload_size_mean: float = 0.0
    payload_size_std: float = 0.0
    known_dest_ips: Set[str] = field(default_factory=set)
    known_dest_ports: Set[int] = field(default_factory=set)
    active_hours: Set[int] = field(default_factory=set)
    baseline_established: bool = False
    baseline_created_at: Optional[float] = None
    baseline_updated_at: Optional[float] = None
    firmware_updated_at: Optional[float] = None
    message_count: int = 0
    enrollment_time: Optional[float] = None

    @property
    def baseline_age_days(self) -> float:
        if self.baseline_created_at is None:
            return 0.0
        return (time.time() - self.baseline_created_at) / 86400.0

    @property
    def firmware_age_days(self) -> float:
        if self.firmware_updated_at is None:
            return 0.0
        return (time.time() - self.firmware_updated_at) / 86400.0

    @property
    def uptime_hours(self) -> float:
        if self.enrollment_time is None:
            return 0.0
        return (time.time() - self.enrollment_time) / 3600.0


class DeviceIDAnonymizer:
    def __init__(self, zone_salt: str = "shieldnet-zone-salt"):
        self.zone_salt = zone_salt

    def anonymize(self, mac_address: str) -> str:
        mac_clean = mac_address.replace(":", "").replace("-", "").upper()
        digest = hmac.new(
            self.zone_salt.encode(),
            mac_clean.encode(),
            hashlib.sha256,
        ).hexdigest()[:8]
        return f"DEV-{digest.upper()}"

    def anonymize_category(self, category: str, device_num: int) -> str:
        prefix_map = {
            "traffic": "TRF",
            "camera": "CAM",
            "energy": "ENR",
            "water": "WTR",
            "emergency": "EMG",
            "environmental": "ENV",
            "other": "OTH",
        }
        prefix = prefix_map.get(category, "DEV")
        return f"{prefix}-{device_num:04d}"


class BaselineBuilder:
    def __init__(self, device_id: str, category: str, protocol: str):
        self.device_id = device_id
        self.category = category
        self.protocol = protocol
        self._msg_rates: list = []
        self._payload_sizes: list = []
        self._dest_ips: set = set()
        self._dest_ports: set = set()
        self._hour_histogram: dict = {}
        self._message_count = 0
        self._start_time = time.time()

    def record_message(self, msg: dict):
        self._message_count += 1
        self._payload_sizes.append(msg.get("payload_size", 0))
        dest_ip = msg.get("dest_ip_hash")
        if dest_ip:
            self._dest_ips.add(dest_ip)
        dest_port = msg.get("dest_port")
        if dest_port:
            self._dest_ports.add(dest_port)
        import datetime
        hour = datetime.datetime.now().hour
        self._hour_histogram[hour] = self._hour_histogram.get(hour, 0) + 1

    def build(self) -> DeviceBaselineProfile:
        import numpy as np
        profile = DeviceBaselineProfile(
            device_id=self.device_id,
            zone_id="",
            category=self.category,
            protocol=self.protocol,
            expected_topic_prefix=f"city//{self.category}/",
            expected_update_hz=1.0,
            firmware_version="0.0.0",
            msg_rate_mean=float(np.mean(self._payload_sizes)) if self._payload_sizes else 0.0,
            msg_rate_std=float(np.std(self._payload_sizes)) if len(self._payload_sizes) > 1 else 0.0,
            payload_size_mean=float(np.mean(self._payload_sizes)) if self._payload_sizes else 0.0,
            payload_size_std=float(np.std(self._payload_sizes)) if len(self._payload_sizes) > 1 else 0.0,
            known_dest_ips=self._dest_ips,
            known_dest_ports=self._dest_ports,
            active_hours=set(h for h, c in self._hour_histogram.items() if c > 0),
            baseline_established=self._message_count >= 1000,
            baseline_created_at=time.time(),
            baseline_updated_at=time.time(),
            enrollment_time=self._start_time,
            message_count=self._message_count,
        )

        rate = self._message_count / ((time.time() - self._start_time) / 60.0 + 1e-8)
        profile.msg_rate_mean = rate
        profile.msg_rate_std = rate * 0.3
        return profile

    def is_ready(self) -> bool:
        return self._message_count >= 1000

    def elapsed_hours(self) -> float:
        return (time.time() - self._start_time) / 3600.0
