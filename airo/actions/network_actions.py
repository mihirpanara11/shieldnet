import logging

logger = logging.getLogger("shieldnet.airo.actions.network")


class NetworkAction:
    def rate_limit_mac(self, mac_address: str, limit_pps: int = 10):
        logger.info(f"Rate-limiting MAC {mac_address} to {limit_pps} pps")

    def move_to_vlan(self, mac_address: str, vlan_id: int):
        logger.info(f"Moving device {mac_address} to VLAN {vlan_id}")

    def quarantine_device(self, mac_address: str):
        self.move_to_vlan(mac_address, 999)
        logger.info(f"Device {mac_address} quarantined to VLAN 999")

    def sandbox_device(self, mac_address: str):
        self.move_to_vlan(mac_address, 998)
        logger.info(f"Device {mac_address} moved to SANDBOX VLAN 998")

    def block_outbound_connections(self, device_ip: str):
        logger.info(f"Blocking outbound connections for {device_ip}")

    def reroute_traffic(self, zone_id: str):
        logger.info(f"Rerouting traffic for zone {zone_id} to backup path")

    def rate_limit_subnet(self, subnet: str):
        logger.info(f"Rate-limiting subnet {subnet}")

    def restore_device(self, mac_address: str):
        self.move_to_vlan(mac_address, 1)
        logger.info(f"Device {mac_address} restored to NORMAL VLAN 1")
