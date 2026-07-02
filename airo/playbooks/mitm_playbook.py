from airo.playbooks.base_playbook import BasePlaybook, PlaybookStep


class MitMPlaybook(BasePlaybook):
    def __init__(self):
        super().__init__("MITM_RESPONSE_v1")

    def build_steps(self, **kwargs):
        self.steps = [
            PlaybookStep("invalidate_sessions", "invalidate_sessions", 0),
            PlaybookStep("force_re_tls_handshake", "force_re_tls_handshake", 100),
            PlaybookStep("enable_certificate_pinning", "enable_certificate_pinning", 200),
            PlaybookStep("block_suspected_interceptor", "block_suspected_interceptor", 300),
            PlaybookStep("alert_soc_mitm", "alert_soc_mitm", 500),
        ]
