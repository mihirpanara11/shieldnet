from airo.playbooks.base_playbook import BasePlaybook, PlaybookStep


class DDoSPlaybook(BasePlaybook):
    def __init__(self):
        super().__init__("DDoS_RESPONSE_v2")

    def build_steps(self, **kwargs):
        self.steps = [
            PlaybookStep("rate_limit_mac", "rate_limit_mac", 0),
            PlaybookStep("publish_isolation_command", "publish_isolation_command", 50),
            PlaybookStep("reroute_traffic", "reroute_traffic", 100),
            PlaybookStep("quarantine_vlan", "quarantine_vlan", 200),
            PlaybookStep("generate_incident_report", "generate_incident_report", 300),
        ]
