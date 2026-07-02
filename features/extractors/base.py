from dataclasses import dataclass, field
from typing import List, Optional
import numpy as np
import time
from collections import deque
import datetime


@dataclass
class DeviceBaseline:
    device_id: str
    category: str
    protocol: str
    msg_rate_mean: float
    msg_rate_std: float
    payload_size_mean: float
    payload_size_std: float
    known_dest_ips: set = field(default_factory=set)
    known_dest_ports: set = field(default_factory=set)
    active_hours: set = field(default_factory=set)
    baseline_age_days: float = 0.0
    firmware_age_days: float = 0.0


class FeatureExtractor:
    def __init__(self, device_id: str, baseline: DeviceBaseline):
        self.device_id = device_id
        self.baseline = baseline
        self._msg_times_1min: deque = deque()
        self._msg_times_5min: deque = deque()
        self._msg_times_1hr: deque = deque()
        self._payload_sizes: deque = deque(maxlen=100)
        self._inter_intervals: deque = deque(maxlen=100)
        self._last_msg_time: Optional[float] = None
        self._connection_count_1min = 0
        self._new_connections_1min = 0
        self._failed_auth_5min = 0
        self._total_bytes_1min = 0.0
        self._total_bytes_5min = 0.0
        self._cumulative_anomaly_24h = 0.0

    def extract(self, raw_msg: dict, now: float = None) -> List[float]:
        if now is None:
            now = time.time()

        self._update_windows(now, raw_msg)

        payload_bytes = raw_msg.get('payload_size', 0)
        entropy = self._calc_entropy(raw_msg.get('payload_sample', b''))
        dt = now - self._last_msg_time if self._last_msg_time else 0.0

        features = [
            float(len(self._msg_times_1min)),
            float(len(self._msg_times_5min)) / 5.0,
            float(len(self._msg_times_1hr)) / 10.0,
            float(len(self._msg_times_1hr)) / 60.0,
            (float(len(self._msg_times_1min)) / (float(len(self._msg_times_5min)) / 5.0 + 1e-8)),
            float(payload_bytes),
            float(np.mean(self._payload_sizes)) if self._payload_sizes else 0.0,
            float(np.std(self._payload_sizes)) if len(self._payload_sizes) > 1 else 0.0,
            self._zscore(payload_bytes, self.baseline.payload_size_mean, self.baseline.payload_size_std),
            entropy,
            entropy - (float(np.mean(self._payload_sizes)) if self._payload_sizes else 0.0),
            self._encode_protocol(raw_msg.get('protocol', 'MQTT')),
            float(raw_msg.get('qos', -1)),
            float(1 if raw_msg.get('retain', False) else 0),
            float(raw_msg.get('topic', '').count('/')),
            float(hash(raw_msg.get('topic_pattern', '')) % 10000),
            float(raw_msg.get('coap_method', -1)),
            float(raw_msg.get('coap_response_class', -1)),
            float(1 if raw_msg.get('dest_ip_hash') in self.baseline.known_dest_ips else 0),
            float(1 if raw_msg.get('dest_ip_is_external', False) else 0),
            float(1 if raw_msg.get('dest_ip_new_in_24h', False) else 0),
            float(raw_msg.get('dest_port', 0)),
            float(1 if raw_msg.get('dest_port') in self.baseline.known_dest_ports else 0),
            float(self._connection_count_1min),
            float(self._new_connections_1min / (self._connection_count_1min + 1e-8)),
            float(self._failed_auth_5min),
            float(self._failed_auth_5min / (len(self._msg_times_5min) + 1e-8)),
            float(1 if raw_msg.get('scan_detected', False) else 0),
            self._total_bytes_1min,
            self._total_bytes_5min,
            self._zscore(self._total_bytes_1min,
                         self.baseline.msg_rate_mean * self.baseline.payload_size_mean,
                         self.baseline.msg_rate_std * self.baseline.payload_size_std),
            float(self._hour_of_day(now)),
            float(self._day_of_week(now)),
            float(1 if self._hour_of_day(now) in self.baseline.active_hours else 0),
            dt,
            float(np.mean(self._inter_intervals)) if self._inter_intervals else 0.0,
            float(np.std(self._inter_intervals)) if len(self._inter_intervals) > 1 else 0.0,
            self._zscore(dt,
                         float(np.mean(self._inter_intervals)) if self._inter_intervals else dt,
                         float(np.std(self._inter_intervals)) if len(self._inter_intervals) > 1 else 1.0),
            float(self._encode_category(self.baseline.category)),
            float(raw_msg.get('device_uptime_hours', 0.0)),
            float(self.baseline.baseline_age_days),
            float(self.baseline.firmware_age_days),
            float(raw_msg.get('zone_alert_level', 0)),
            float(raw_msg.get('zone_peer_anomaly_rate', 0.0)),
            float(raw_msg.get('response_time_ms', 0.0)),
            self._zscore(raw_msg.get('response_time_ms', 0.0), 50.0, 20.0),
        ]

        features.append(0.40 * features[0] + 0.30 * features[1] + 0.30 * features[2])

        assert len(features) == 47, f"Expected 47 features, got {len(features)}"
        self._last_msg_time = now
        return features

    def _zscore(self, x, mean, std):
        return float(np.clip((x - mean) / (std + 1e-8), -5.0, 5.0))

    def _calc_entropy(self, payload: bytes) -> float:
        if not payload:
            return 0.0
        counts = np.bincount(np.frombuffer(payload, dtype=np.uint8), minlength=256)
        probs = counts[counts > 0] / len(payload)
        return float(-np.sum(probs * np.log2(probs)))

    def _encode_protocol(self, protocol: str) -> float:
        return float({'MQTT': 0, 'CoAP': 1, 'Zigbee': 2,
                       'Z-Wave': 3, 'LoRaWAN': 4}.get(protocol, 5))

    def _encode_category(self, category: str) -> float:
        return float({'traffic': 0, 'camera': 1, 'energy': 2, 'water': 3,
                       'emergency': 4, 'environmental': 5}.get(category, 6))

    def _hour_of_day(self, ts):
        return datetime.datetime.fromtimestamp(ts).hour

    def _day_of_week(self, ts):
        return datetime.datetime.fromtimestamp(ts).weekday()

    def update_cumulative_anomaly(self, score: float):
        self._cumulative_anomaly_24h += score

    def reset_cumulative_anomaly(self):
        self._cumulative_anomaly_24h = 0.0

    def _update_windows(self, now: float, raw_msg: dict):
        cutoff_1min = now - 60
        cutoff_5min = now - 300
        cutoff_1hr = now - 3600
        while self._msg_times_1min and self._msg_times_1min[0] < cutoff_1min:
            self._msg_times_1min.popleft()
        while self._msg_times_5min and self._msg_times_5min[0] < cutoff_5min:
            self._msg_times_5min.popleft()
        while self._msg_times_1hr and self._msg_times_1hr[0] < cutoff_1hr:
            self._msg_times_1hr.popleft()
        self._msg_times_1min.append(now)
        self._msg_times_5min.append(now)
        self._msg_times_1hr.append(now)
        payload_bytes = raw_msg.get('payload_size', 0)
        self._payload_sizes.append(payload_bytes)
        self._total_bytes_1min += payload_bytes
        self._total_bytes_5min += payload_bytes
        if self._last_msg_time:
            self._inter_intervals.append(now - self._last_msg_time)
