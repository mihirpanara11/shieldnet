class ZigbeeExtractor:
    def extract(self, raw_msg: dict) -> dict:
        return {
            "protocol": "Zigbee",
            "payload_size": raw_msg.get("payload_size", 0),
            "dest_port": raw_msg.get("dest_port", 0),
            "zigbee_cluster": raw_msg.get("zigbee_cluster_id", 0),
            "zigbee_profile": raw_msg.get("zigbee_profile_id", 0),
            "zigbee_command": raw_msg.get("zigbee_command", 0),
        }

    def detect_anomalies(self, cluster_id: int, expected_clusters: list) -> list:
        flags = []
        if cluster_id not in expected_clusters:
            flags.append(f"UNEXPECTED_CLUSTER_{cluster_id}")
        return flags
