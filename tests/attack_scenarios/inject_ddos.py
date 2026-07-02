import argparse
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("shieldnet.test.ddos")


def inject_ddos(target_device: str, zone: str, duration: int):
    logger.info(f"Injecting DDoS attack on {target_device} in {zone} for {duration}s")
    logger.info(f"  Simulating Mirai-style TCP flood traffic")
    for second in range(duration):
        if second % 5 == 0:
            rate = min(100 + second * 10, 1000)
            logger.info(f"  t={second}s: Sending {rate} pkt/s to {target_device}")
        time.sleep(1)
    logger.info("DDoS injection complete")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-device", required=True)
    parser.add_argument("--zone", default="ZONE-04")
    parser.add_argument("--duration", type=int, default=30)
    args = parser.parse_args()
    inject_ddos(args.target_device, args.zone, args.duration)
