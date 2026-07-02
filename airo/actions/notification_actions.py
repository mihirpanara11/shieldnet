import logging
import json

logger = logging.getLogger("shieldnet.airo.actions.notification")


class NotificationAction:
    def __init__(self, soc_webhook: str = ""):
        self.soc_webhook = soc_webhook
        self._alert_callbacks = []

    def register_callback(self, callback):
        self._alert_callbacks.append(callback)

    def alert_soc(self, incident_report: dict, priority: int = 3):
        logger.info(f"[PRIORITY {priority}] SOC Alert: {incident_report.get('incident_id', '')}")
        for cb in self._alert_callbacks:
            try:
                cb(incident_report, priority)
            except Exception:
                pass

    def push_network_wide_alert(self, message: str):
        logger.info(f"NETWORK-WIDE ALERT: {message}")

    def broadcast_threat_intel(self, intel_data: dict):
        logger.info(f"Broadcasting threat intel: {intel_data.get('intel_type', '')}")

    def page_on_call_engineer(self, incident_id: str, message: str = ""):
        logger.info(f"PAGING on-call engineer for incident {incident_id}: {message}")

    def send_webhook(self, payload: dict):
        logger.info(f"Webhook sent to {self.soc_webhook}")
