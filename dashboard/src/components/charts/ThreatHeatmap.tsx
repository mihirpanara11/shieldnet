import React from 'react';

interface ZoneData {
  zone_id: string;
  alert_level: 0 | 1 | 2 | 3;
  device_count: number;
  active_alerts: number;
  last_alert: string;
}

interface ThreatHeatmapProps {
  zones: ZoneData[];
}

const LEVEL_COLORS: Record<number, string> = {
  0: '#2E7D32',
  1: '#F9A825',
  2: '#E65100',
  3: '#C62828',
};

export const ThreatHeatmap: React.FC<ThreatHeatmapProps> = ({ zones }) => {
  return (
    <div style={{ background: 'white', borderRadius: '8px', padding: '16px', boxShadow: '0 2px 8px rgba(0,0,0,0.08)' }}>
      <h3 style={{ fontFamily: 'Cambria, serif', color: '#004D40', margin: '0 0 16px 0', fontSize: '18px' }}>
        Zone Threat Heatmap
      </h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: '12px' }}>
        {zones.map(zone => (
          <div key={zone.zone_id}
               style={{
                 background: LEVEL_COLORS[zone.alert_level],
                 borderRadius: '8px',
                 padding: '16px',
                 color: 'white',
                 fontFamily: 'Calibri, sans-serif',
                 cursor: 'pointer',
                 transition: 'transform 0.2s',
               }}
               title={`${zone.zone_id}: ${zone.device_count} devices, ${zone.active_alerts} alerts`}>
            <div style={{ fontSize: '16px', fontWeight: 700 }}>{zone.zone_id}</div>
            <div style={{ fontSize: '12px', opacity: 0.9, marginTop: '8px' }}>
              {zone.device_count} devices
            </div>
            <div style={{ fontSize: '12px', opacity: 0.9 }}>
              {zone.active_alerts} alerts
            </div>
            <div style={{ fontSize: '10px', opacity: 0.7, marginTop: '8px' }}>
              Last: {zone.last_alert}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
