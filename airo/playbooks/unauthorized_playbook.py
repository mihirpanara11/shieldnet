from airo.playbooks.base_playbook import BasePlaybook, PlaybookStep


class UnauthorizedPlaybook(BasePlaybook):
    def __init__(self):
        super().__init__("UNAUTHORIZED_RESPONSE_v1")

    def build_steps(self, **kwargs):
        self.steps = [
            PlaybookStep("revoke_auth_tokens", "revoke_auth_tokens", 0),
            PlaybookStep("block_device_mqtt_acl", "block_device_mqtt_acl", 100),
            PlaybookStep("force_tls_rotation", "force_tls_rotation", 200),
            PlaybookStep("require_reauth_mfa", "require_reauth_mfa", 300),
            PlaybookStep("log_auth_attempts_24h", "log_auth_attempts_24h", 500),
            PlaybookStep("alert_soc_unauthorized", "alert_soc_unauthorized", 1000),
        ]
