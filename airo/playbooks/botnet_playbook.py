from airo.playbooks.base_playbook import BasePlaybook, PlaybookStep


class BotnetPlaybook(BasePlaybook):
    def __init__(self):
        super().__init__("BOTNET_RESPONSE_v1")

    def build_steps(self, **kwargs):
        self.steps = [
            PlaybookStep("block_outbound_c2", "block_outbound_connections", 0),
            PlaybookStep("move_to_sandbox_vlan", "move_to_sandbox_vlan", 100),
            PlaybookStep("start_packet_capture", "start_packet_capture", 200),
            PlaybookStep("broadcast_threat_intel", "broadcast_threat_intel", 500),
            PlaybookStep("alert_soc", "alert_soc_botnet", 1000),
        ]
