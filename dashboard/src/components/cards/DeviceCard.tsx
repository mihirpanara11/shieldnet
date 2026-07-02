import React from 'react';

interface DeviceCardProps {
  deviceId: string;
  category: string;
  zoneId: string;
  status: string;
  lastSeen: string;
  anomalyScore: number;
}

const STATUS_COLORS: Record<string, string> = {
  NORMAL: '#2E7D32',
  SUSPICIOUS: '#F9A825',
  CONTAINED: '#C62828',
  OFFLINE: '#78909C',
};

export const DeviceCard: React.FC<DeviceCardProps> = ({
  deviceId, category, zoneId, status, lastSeen, anomalyScore,
}) => {
  return (
    <div style={{
      background: 'white',
      borderRadius: '8px',
      padding: '16px',
      borderTop: '4px solid #00695C',
      boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
      cursor: 'pointer',
      fontFamily: 'Calibri, sans-serif',
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: '13px', fontWeight: 700, color: '#004D40' }}>
          {deviceId}
        </span>
        <span style={{
          fontSize: '11px', padding: '2px 8px', borderRadius: '12px',
          background: `${STATUS_COLORS[status]}22`,
          color: STATUS_COLORS[status],
          fontWeight: 700,
        }}>
          {status}
        </span>
      </div>
      <div style={{ fontSize: '12px', color: '#37474F', marginTop: '8px' }}>
        {category.replace('_', ' ')} · {zoneId}
      </div>
      <div style={{ fontSize: '11px', color: '#78909C', marginTop: '4px' }}>
        Last seen: {lastSeen}
      </div>
      <div style={{ marginTop: '8px', fontSize: '12px', color: anomalyScore > 0.5 ? '#C62828' : '#2E7D32' }}>
        Score: {(anomalyScore * 100).toFixed(1)}%
      </div>
    </div>
  );
};
