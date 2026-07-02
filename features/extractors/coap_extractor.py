class CoAPExtractor:
    METHOD_MAP = {"GET": 1, "POST": 2, "PUT": 3, "DELETE": 4}

    def extract(self, raw_msg: dict) -> dict:
        method_str = raw_msg.get("coap_method", "GET")
        method_code = self.METHOD_MAP.get(method_str, -1)
        response_code = raw_msg.get("coap_response_code", 0)
        if response_code >= 200 and response_code < 300:
            resp_class = 2
        elif response_code >= 400 and response_code < 500:
            resp_class = 4
        elif response_code >= 500 and response_code < 600:
            resp_class = 5
        else:
            resp_class = -1

        return {
            "coap_method": method_code,
            "coap_response_class": resp_class,
            "protocol": "CoAP",
            "payload_size": raw_msg.get("payload_size", 0),
            "dest_port": raw_msg.get("dest_port", 5683),
            "observe_option": raw_msg.get("coap_observe", False),
            "blockwise": raw_msg.get("coap_blockwise", False),
        }

    def detect_anomalies(self, method: str, expected_methods: list) -> list:
        flags = []
        if method not in expected_methods:
            flags.append(f"UNEXPECTED_METHOD_{method}")
        return flags
