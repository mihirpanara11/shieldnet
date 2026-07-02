import React from 'react';

type DeviceStatus = 'online' | 'degraded' | 'offline' | 'quarantined';

interface Device {
  id: string; category: string; zone: string; protocol: string;
  status: DeviceStatus; lastSeen: string; anomalyScore: number; alerts24h: number;
}

const mockDevices: Device[] = [
  { id: 'TRF-0042', category: 'Traffic Sensor', zone: 'ZONE-04', protocol: 'MQTT', status: 'online', lastSeen: '30s ago', anomalyScore: 0.12, alerts24h: 0 },
  { id: 'TRF-0043', category: 'Traffic Sensor', zone: 'ZONE-04', protocol: 'MQTT', status: 'online', lastSeen: '12s ago', anomalyScore: 0.08, alerts24h: 0 },
  { id: 'CAM-0007', category: 'Camera', zone: 'ZONE-02', protocol: 'MQTT', status: 'degraded', lastSeen: '2m ago', anomalyScore: 0.45, alerts24h: 3 },
  { id: 'CAM-0012', category: 'Camera', zone: 'ZONE-04', protocol: 'MQTT', status: 'quarantined', lastSeen: '15m ago', anomalyScore: 0.91, alerts24h: 8 },
  { id: 'ENR-0007', category: 'Energy Meter', zone: 'ZONE-01', protocol: 'CoAP', status: 'online', lastSeen: '1m ago', anomalyScore: 0.21, alerts24h: 1 },
  { id: 'ENR-0012', category: 'Energy Meter', zone: 'ZONE-03', protocol: 'CoAP', status: 'offline', lastSeen: '1h ago', anomalyScore: 0.0, alerts24h: 0 },
  { id: 'LGT-0001', category: 'Street Light', zone: 'ZONE-01', protocol: 'Zigbee', status: 'online', lastSeen: '45s ago', anomalyScore: 0.03, alerts24h: 0 },
  { id: 'WTR-0003', category: 'Water Valve', zone: 'ZONE-03', protocol: 'LoRaWAN', status: 'online', lastSeen: '5m ago', anomalyScore: 0.15, alerts24h: 0 },
];

const statusColors: Record<DeviceStatus, string> = {
  online: '#2E7D32', degraded: '#E65100', offline: '#78909C', quarantined: '#C62828',
};

const statusBg: Record<DeviceStatus, string> = {
  online: '#E8F5E9', degraded: '#FFF3E0', offline: '#ECEFF1', quarantined: '#FFEBEE',
};

const Devices: React.FC = () => {
  const online = mockDevices.filter(d => d.status === 'online').length;
  const degraded = mockDevices.filter(d => d.status === 'degraded').length;
  const quarantined = mockDevices.filter(d => d.status === 'quarantined').length;
  const offline = mockDevices.filter(d => d.status === 'offline').length;

  return (
    <div style={{ fontFamily: 'Calibri, sans-serif' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1 style={{ fontFamily: 'Cambria, serif', color: '#004D40', margin: 0 }}>Device Management</h1>
        <input placeholder="Search devices..." style={{
          padding: '8px 16px', border: '1px solid #CFD8DC', borderRadius: '4px',
          fontFamily: 'Calibri, sans-serif', fontSize: '13px', width: '280px',
        }} />
      </div>
      <div style={{ display: 'flex', gap: '16px', marginBottom: '24px' }}>
        {[
          { label: 'Online', value: online, color: '#2E7D32', bg: '#E8F5E9' },
          { label: 'Degraded', value: degraded, color: '#E65100', bg: '#FFF3E0' },
          { label: 'Quarantined', value: quarantined, color: '#C62828', bg: '#FFEBEE' },
          { label: 'Offline', value: offline, color: '#78909C', bg: '#ECEFF1' },
        ].map(k => (
          <div key={k.label} style={{
            flex: 1, borderTop: `4px solid ${k.color}`, background: k.bg,
            borderRadius: '8px', padding: '16px 20px', boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
          }}>
            <div style={{ fontSize: '36px', fontWeight: 700, fontFamily: 'Cambria, serif', color: k.color }}>{k.value}</div>
            <div style={{ fontSize: '12px', fontWeight: 700, color: '#37474F', textTransform: 'uppercase', letterSpacing: '0.04em' }}>{k.label}</div>
          </div>
        ))}
      </div>
      <div style={{ background: 'white', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.08)', overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#004D40', color: 'white' }}>
              {['Device ID', 'Category', 'Zone', 'Protocol', 'Status', 'Last Seen', 'Anomaly', 'Alerts/24h'].map(h => (
                <th key={h} style={{ padding: '12px 16px', textAlign: 'left', fontSize: '12px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.04em' }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {mockDevices.map((d, i) => (
              <tr key={d.id} style={{ background: i % 2 === 0 ? '#E0F2F1' : 'white', borderBottom: '1px solid #ECEFF1' }}>
                <td style={{ padding: '10px 16px', fontSize: '13px', fontWeight: 700, fontFamily: 'Consolas, monospace', color: '#004D40' }}>{d.id}</td>
                <td style={{ padding: '10px 16px', fontSize: '12px', color: '#37474F' }}>{d.category}</td>
                <td style={{ padding: '10px 16px', fontSize: '12px', color: '#37474F' }}>{d.zone}</td>
                <td style={{ padding: '10px 16px', fontSize: '11px', color: '#78909C', fontWeight: 700 }}>{d.protocol}</td>
                <td style={{ padding: '10px 16px' }}>
                  <span style={{ padding: '2px 10px', borderRadius: '12px', fontWeight: 700, fontSize: '11px', background: statusBg[d.status], color: statusColors[d.status] }}>{d.status}</span>
                </td>
                <td style={{ padding: '10px 16px', fontSize: '12px', color: '#78909C' }}>{d.lastSeen}</td>
                <td style={{ padding: '10px 16px', fontSize: '12px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <div style={{ width: '40px', height: '6px', background: '#ECEFF1', borderRadius: '3px', overflow: 'hidden' }}>
                      <div style={{ width: `${d.anomalyScore * 100}%`, height: '100%', background: d.anomalyScore > 0.7 ? '#C62828' : d.anomalyScore > 0.4 ? '#E65100' : '#2E7D32', borderRadius: '3px' }} />
                    </div>
                    {(d.anomalyScore * 100).toFixed(0)}%
                  </div>
                </td>
                <td style={{ padding: '10px 16px', fontSize: '12px', fontWeight: 700, color: d.alerts24h > 5 ? '#C62828' : d.alerts24h > 0 ? '#E65100' : '#2E7D32' }}>{d.alerts24h}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Devices;
