from airo.playbooks.base_playbook import BasePlaybook, PlaybookStep


class RansomwarePlaybook(BasePlaybook):
    def __init__(self):
        super().__init__("RANSOMWARE_RESPONSE_v1")

    def build_steps(self, **kwargs):
        self.steps = [
            PlaybookStep("push_network_wide_alert", "push_network_wide_alert", 0),
            PlaybookStep("immediately_isolate_device", "immediately_isolate_device", 0),
            PlaybookStep("snapshot_to_encrypted_storage", "snapshot_to_encrypted_storage", 100),
            PlaybookStep("initiate_lateral_scan", "initiate_lateral_scan", 200),
            PlaybookStep("rate_limit_affected_subnet", "rate_limit_affected_subnet", 500),
            PlaybookStep("page_on_call_engineer", "page_on_call_engineer", 1000),
        ]
