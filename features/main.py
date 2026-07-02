import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("shieldnet.features")


def run_feature_service():
    logger.info("ShieldNet Feature Extraction Service starting...")
    from features.extractors.mqtt_extractor import MQTTExtractor
    from features.extractors.coap_extractor import CoAPExtractor
    from features.extractors.lorawan_extractor import LoRaWANExtractor
    from features.extractors.zigbee_extractor import ZigbeeExtractor
    from features.normalization import OnlineNormalizer

    mqtt = MQTTExtractor()
    coap = CoAPExtractor()
    lorawan = LoRaWANExtractor()
    zigbee = ZigbeeExtractor()
    normalizer = OnlineNormalizer(47)

    logger.info("Feature Extraction Service ready")
    logger.info(f"  Extractors: MQTT, CoAP, LoRaWAN, Zigbee")
    logger.info(f"  Normalizer: 47 features, online Welford")

    return {
        "mqtt_extractor": mqtt,
        "coap_extractor": coap,
        "lorawan_extractor": lorawan,
        "zigbee_extractor": zigbee,
        "normalizer": normalizer,
    }


if __name__ == "__main__":
    run_feature_service()
