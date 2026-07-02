import argparse
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("shieldnet.test.scan")


def inject_scan(target_device: str, zone: str, ports: list):
    logger.info(f"Injecting port scan on {target_device} in {zone}")
    logger.info(f"  Scanning ports: {ports[0]}-{ports[-1]}")
    for port in ports:
        logger.info(f"  Scanning port {port}/tcp on {target_device}")
        time.sleep(1)
    logger.info("Scan injection complete")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-device", default="TRF-0042")
    parser.add_argument("--zone", default="ZONE-04")
    args = parser.parse_args()
    ports = list(range(1, 1025))
    inject_scan(args.target_device, args.zone, ports)
