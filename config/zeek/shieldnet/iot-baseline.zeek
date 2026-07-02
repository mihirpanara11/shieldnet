module IoT_Baseline;

export {
  redef enum Log::ID += { LOG };

  type BaselineInfo: record {
    ts:             time     &log;
    device_hash:    string   &log;
    protocol:       string   &log;
    msg_count_1min: count    &log;
    payload_avg:    double   &log;
    dest_ips:       count    &log;
  };
}

global device_msg_count: table[string] of count &default=0;
global device_payload_total: table[string] of double &default=0.0;
global device_dest_ips: table[string] of set[addr] &default=table();
global device_window_start: table[string] of time &default=network_time();

event mqtt_publish(c: connection, is_orig: bool, msg_type: count, body: MQTT::PublishMsg)
{
  local device_id = md5_hmac(c$id$orig_h + "", "shieldnet-baseline-salt");
  device_msg_count[device_id] += 1;
  device_payload_total[device_id] += |body$payload|;
  add device_dest_ips[device_id][c$id$resp_h];

  if ( network_time() - device_window_start[device_id] > 60sec ) {
    local info = BaselineInfo($ts=network_time(),
                              $device_hash=device_id,
                              $protocol="MQTT",
                              $msg_count_1min=device_msg_count[device_id],
                              $payload_avg=device_payload_total[device_id] / (device_msg_count[device_id] + 1),
                              $dest_ips=|device_dest_ips[device_id]|);
    Log::write(IoT_Baseline::LOG, info);
    device_msg_count[device_id] = 0;
    device_payload_total[device_id] = 0.0;
    delete device_dest_ips[device_id];
    device_window_start[device_id] = network_time();
  }
}
