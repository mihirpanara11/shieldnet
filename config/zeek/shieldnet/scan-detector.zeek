module ScanDetector;

export {
  redef enum Log::ID += { LOG };

  type ScanInfo: record {
    ts:            time     &log;
    src_hash:      string   &log;
    dst_ips:       count    &log;
    dst_ports:     count    &log;
    is_sequential: bool     &log;
  };
}

global scan_src: table[string] of set[addr] &default=table();
global scan_ports: table[string] of set[port] &default=table();
global scan_window: table[string] of time &default=network_time();

event connection_attempt(c: connection)
{
  local src_hash = md5_hmac(c$id$orig_h + "", "shieldnet-scan-salt");
  add scan_src[src_hash][c$id$resp_h];
  add scan_ports[src_hash][c$id$resp_p];

  if ( network_time() - scan_window[src_hash] > 60sec ) {
    local dst_count = |scan_src[src_hash]|;
    local port_count = |scan_ports[src_hash]|;
    local is_seq = port_count > 20;

    if ( dst_count > 5 || port_count > 10 ) {
      local info = ScanInfo($ts=network_time(),
                            $src_hash=src_hash,
                            $dst_ips=dst_count,
                            $dst_ports=port_count,
                            $is_sequential=is_seq);
      Log::write(ScanDetector::LOG, info);
    }

    delete scan_src[src_hash];
    delete scan_ports[src_hash];
    scan_window[src_hash] = network_time();
  }
}
