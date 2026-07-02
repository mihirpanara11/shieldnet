import time
import logging
from fl_client.client import FLClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("shieldnet.fl.client.main")


def run_fl_client(zone_id: str, fl_server_address: str,
                  fl_server_port: int = 9080,
                  interval_minutes: int = 60,
                  local_epochs: int = 3):
    client = FLClient(zone_id, local_epochs=local_epochs)
    logger.info(f"FL Client for zone {zone_id} started. "
                 f"Server: {fl_server_address}:{fl_server_port}, "
                 f"interval: {interval_minutes}min")

    while True:
        try:
            logger.info(f"Starting FL round for zone {zone_id}")
            result = client.train_local()
            logger.info(f"Round complete - loss: {result.get('loss', 0):.4f}, "
                         f"samples: {result.get('samples', 0)}")
        except Exception as e:
            logger.error(f"FL round failed: {e}")

        time.sleep(interval_minutes * 60)
