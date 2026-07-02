from typing import Optional


class MQTTExtractor:
    def extract(self, raw_msg: dict) -> dict:
        return {
            "client_id_hash": self._hash_client_id(raw_msg.get("client_id", "")),
            "topic": raw_msg.get("topic", ""),
            "qos": raw_msg.get("qos", -1),
            "retain": raw_msg.get("retain", False),
            "payload_size": raw_msg.get("payload_size", 0),
            "protocol": "MQTT",
            "topic_depth": raw_msg.get("topic", "").count("/"),
            "topic_pattern_hash": hash(raw_msg.get("topic", "")) % 10000,
            "dest_port": raw_msg.get("dest_port", 1883),
        }

    def detect_anomalies(self, topic: str, qos: int, retain: bool, payload_size: int,
                         client_id: str, expected_prefix: str) -> list:
        flags = []
        if topic.startswith("$SYS"):
            flags.append("SYSTEM_TOPIC_PUBLISH")
        if "#" in topic or "+" in topic:
            flags.append("WILDCARD_IN_PUBLISH")
        if not topic.startswith(expected_prefix):
            flags.append("UNEXPECTED_TOPIC_PREFIX")
        if payload_size > 10000:
            flags.append("OVERSIZED_PAYLOAD")
        if qos == 0:
            flags.append("QOS0_UNEXPECTED")
        if retain:
            flags.append("RETAIN_FLAG_UNEXPECTED")
        return flags

    def _hash_client_id(self, client_id: str) -> str:
        import hashlib
        return hashlib.sha256(client_id.encode()).hexdigest()[:16]
