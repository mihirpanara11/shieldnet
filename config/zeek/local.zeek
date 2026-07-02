@load base/protocols/conn
@load base/protocols/mqtt
@load base/protocols/dns
@load base/protocols/http
@load base/protocols/ssl

@load ./shieldnet/iot-baseline.zeek
@load ./shieldnet/mqtt-anomaly.zeek
@load ./shieldnet/scan-detector.zeek

@load tuning/json-logs

redef exit_only_after_terminate = T;
redef Cluster::manager_is_logger = F;
