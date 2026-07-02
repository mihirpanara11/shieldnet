module MQTT_Anomaly;

export {
  redef enum Log::ID += { LOG };

  type Info: record {
    ts:             time     &log;
    client_id_hash: string   &log;
    topic:          string   &log;
    qos:            count    &log;
    retain:         bool     &log;
    payload_size:   count    &log;
    anomaly_flags:  set[string] &log &default=set();
  };
}

global client_msg_count: table[string] of count &default=0;
global client_last_reset: table[string] of time &default=network_time();

event mqtt_publish(c: connection, is_orig: bool,
                   msg_type: count, body: MQTT::PublishMsg)
{
  local client_hash = md5_hmac(c$id$orig_h + "", "shieldnet-zone-salt");
  local info = Info($ts=network_time(),
                    $client_id_hash=client_hash,
                    $topic=body$topic,
                    $qos=body$qos,
                    $retain=body$retain,
                    $payload_size=|body$payload|);

  if ( /^\$SYS/ in body$topic )
    add info$anomaly_flags["SYSTEM_TOPIC_PUBLISH"];

  if ( /[#+]/ in body$topic )
    add info$anomaly_flags["WILDCARD_IN_PUBLISH"];

  client_msg_count[client_hash] += 1;
  if ( network_time() - client_last_reset[client_hash] > 10sec ) {
    if ( client_msg_count[client_hash] > 100 )
      add info$anomaly_flags["PUBLISH_FLOOD"];
    client_msg_count[client_hash] = 0;
    client_last_reset[client_hash] = network_time();
  }

  if ( |body$payload| > 10000 )
    add info$anomaly_flags["OVERSIZED_PAYLOAD"];

  Log::write(MQTT_Anomaly::LOG, info);
}
