class LoRaWANExtractor:
    def extract(self, raw_msg: dict) -> dict:
        return {
            "protocol": "LoRaWAN",
            "payload_size": raw_msg.get("payload_size", 0),
            "dest_port": raw_msg.get("dest_port", 0),
            "frame_counter": raw_msg.get("lorawan_fcnt", 0),
            "message_type": raw_msg.get("lorawan_mtype", "Unconfirmed"),
            "data_rate": raw_msg.get("lorawan_datarate", 0),
            "rssi": raw_msg.get("lorawan_rssi", 0.0),
            "snr": raw_msg.get("lorawan_snr", 0.0),
        }

    def detect_anomalies(self, fcnt_current: int, fcnt_previous: int,
                         rssi: float, rssi_baseline: float) -> list:
        flags = []
        if fcnt_current <= fcnt_previous:
            flags.append("FRAME_COUNTER_REPLAY")
        if abs(rssi - rssi_baseline) > 20:
            flags.append("ABNORMAL_RSSI")
        return flags
