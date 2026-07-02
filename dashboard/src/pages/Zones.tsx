import React from 'react';

const zones = [
  { id: 'ZONE-01', name: 'North District', devices: 342, online: 338, degraded: 2, offline: 2, quarantined: 0, alerts: 0, severity: 'low' as const, lastEvent: 'Clean — 2h ago' },
  { id: 'ZONE-02', name: 'East District', devices: 287, online: 280, degraded: 4, offline: 2, quarantined: 1, alerts: 1, severity: 'medium' as const, lastEvent: 'Botnet beacon — 15m ago' },
  { id: 'ZONE-03', name: 'South District', devices: 156, online: 155, degraded: 0, offline: 1, quarantined: 0, alerts: 0, severity: 'low' as const, lastEvent: 'Clean — 1h ago' },
  { id: 'ZONE-04', name: 'Central Hub', devices: 398, online: 385, degraded: 6, offline: 4, quarantined: 3, alerts: 3, severity: 'high' as const, lastEvent: 'DDoS attack — 2m ago' },
  { id: 'ZONE-05', name: 'West District', devices: 211, online: 210, degraded: 1, offline: 0, quarantined: 0, alerts: 0, severity: 'low' as const, lastEvent: 'Clean — 30m ago' },
];

const severityColors = { low: '#2E7D32', medium: '#E65100', high: '#C62828' };
const severityBg = { low: '#E8F5E9', medium: '#FFF3E0', high: '#FFEBEE' };

const Zones: React.FC = () => {
  return (
    <div style={{ fontFamily: 'Calibri, sans-serif' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1 style={{ fontFamily: 'Cambria, serif', color: '#004D40', margin: 0 }}>Zone Overview</h1>
        <div style={{ fontSize: '13px', color: '#78909C' }}>
          Total: <strong style={{ color: '#004D40' }}>{zones.reduce((s, z) => s + z.devices, 0)}</strong> devices across <strong style={{ color: '#004D40' }}>{zones.length}</strong> zones
        </div>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: '16px' }}>
        {zones.map(z => (
          <div key={z.id} style={{
            background: 'white', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
            borderLeft: `6px solid ${severityColors[z.severity]}`,
          }}>
            <div style={{ padding: '20px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                <div>
                  <div style={{ fontSize: '18px', fontWeight: 700, fontFamily: 'Cambria, serif', color: '#004D40' }}>{z.name}</div>
                  <div style={{ fontSize: '12px', color: '#78909C', fontFamily: 'Consolas, monospace' }}>{z.id}</div>
                </div>
                <span style={{
                  padding: '4px 12px', borderRadius: '12px', fontWeight: 700, fontSize: '11px',
                  background: severityBg[z.severity], color: severityColors[z.severity],
                  textTransform: 'uppercase',
                }}>
                  {z.severity}
                </span>
              </div>
              <div style={{ fontSize: '42px', fontWeight: 700, fontFamily: 'Cambria, serif', color: '#00695C', marginBottom: '16px' }}>
                {z.devices}
                <span style={{ fontSize: '14px', color: '#78909C', fontFamily: 'Calibri, sans-serif', marginLeft: '8px', fontWeight: 400 }}>devices</span>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '16px' }}>
                {[
                  { label: 'Online', value: z.online, color: '#2E7D32' },
                  { label: 'Degraded', value: z.degraded, color: '#E65100' },
                  { label: 'Quarantined', value: z.quarantined, color: '#C62828' },
                  { label: 'Offline', value: z.offline, color: '#78909C' },
                ].map(s => (
                  <div key={s.label}>
                    <div style={{ fontSize: '22px', fontWeight: 700, color: s.color, fontFamily: 'Cambria, serif' }}>{s.value}</div>
                    <div style={{ fontSize: '11px', color: '#78909C', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.04em' }}>{s.label}</div>
                  </div>
                ))}
              </div>
              {z.alerts > 0 && (
                <div style={{
                  background: severityBg[z.severity], borderRadius: '6px', padding: '10px 14px',
                  fontSize: '12px', color: severityColors[z.severity], fontWeight: 600,
                }}>
                  {z.alerts} active alerts · {z.lastEvent}
                </div>
              )}
              {z.alerts === 0 && (
                <div style={{
                  background: '#E0F2F1', borderRadius: '6px', padding: '10px 14px',
                  fontSize: '12px', color: '#00695C', fontWeight: 600,
                }}>
                  {z.lastEvent}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Zones;
