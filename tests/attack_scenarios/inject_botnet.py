import argparse
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("shieldnet.test.botnet")


def inject_botnet(zone: str, device_count: int, c2_interval: int):
    logger.info(f"Injecting botnet attack in {zone} with {device_count} devices")
    for i in range(device_count):
        device = f"DEV-{1000 + i}"
        logger.info(f"  Device {device}: Establishing C2 channel (interval={c2_interval}s)")
    for round_num in range(5):
        logger.info(f"  C2 round {round_num + 1}/5: All {device_count} devices beaconing")
        time.sleep(c2_interval)
    logger.info("Botnet injection complete")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--zone", default="ZONE-04")
    parser.add_argument("--device-count", type=int, default=5)
    parser.add_argument("--c2-interval", type=int, default=10)
    parser.add_argument("--target-device", help="Alias for --zone with single device (ignored)")
    args = parser.parse_args()
    inject_botnet(args.zone, args.device_count, args.c2_interval)
