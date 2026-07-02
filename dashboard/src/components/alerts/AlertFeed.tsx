import React, { useEffect, useRef, useState } from 'react';

interface Alert {
  incident_id: string;
  timestamp_detected: string;
  zone_id: string;
  device_category: string;
  threat_class: string;
  score_ensemble: number;
  decision: string;
  status: string;
}

const DECISION_COLORS: Record<string, string> = {
  THREAT_HIGH:   '#C62828',
  THREAT_MEDIUM: '#E65100',
  SUSPICIOUS:    '#F9A825',
  NORMAL:        '#2E7D32',
};

export const AlertFeed: React.FC = () => {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [userScrolled, setUserScrolled] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:3001/ws/alerts');
    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        if (msg.event === 'NEW_THREAT') {
          setAlerts(prev => [msg.data, ...prev].slice(0, 100));
          if (!userScrolled && containerRef.current) {
            containerRef.current.scrollTop = 0;
          }
        }
      } catch {}
    };
    return () => ws.close();
  }, [userScrolled]);

  return (
    <div style={{ height: '400px', overflowY: 'auto', position: 'relative' }}
         ref={containerRef}
         onScroll={e => setUserScrolled((e.target as HTMLDivElement).scrollTop > 20)}>

      {userScrolled && (
        <div style={{
          position: 'sticky', top: 0, background: '#FF8F00',
          color: 'white', textAlign: 'center', padding: '6px',
          fontSize: '12px', cursor: 'pointer', zIndex: 10,
          fontFamily: 'Calibri, sans-serif',
        }} onClick={() => {
          containerRef.current!.scrollTop = 0;
          setUserScrolled(false);
        }}>
          ↑ New alerts above — click to scroll up
        </div>
      )}

      {alerts.map(alert => (
        <div key={alert.incident_id}
             style={{
               display: 'flex', alignItems: 'center',
               padding: '10px 14px',
               borderLeft: `4px solid ${DECISION_COLORS[alert.decision] ?? '#78909C'}`,
               borderBottom: '1px solid #ECEFF1',
               gap: '12px',
               backgroundColor: 'white',
               fontFamily: 'Calibri, sans-serif',
             }}>
          <span style={{ fontSize: '11px', color: '#78909C', width: '80px', flexShrink: 0 }}>
            {new Date(alert.timestamp_detected).toLocaleTimeString()}
          </span>
          <span style={{ fontSize: '12px', fontWeight: 700, color: '#004D40', width: '70px' }}>
            {alert.zone_id}
          </span>
          <span style={{ fontSize: '12px', color: '#37474F', width: '100px' }}>
            {alert.device_category.replace('_', ' ')}
          </span>
          <span style={{
            fontSize: '12px', fontWeight: 700,
            color: DECISION_COLORS[alert.decision] ?? '#78909C', width: '90px',
          }}>
            {alert.threat_class}
          </span>
          <span style={{
            fontSize: '12px', fontWeight: 700,
            color: alert.score_ensemble >= 0.85 ? '#C62828' : '#E65100', width: '50px',
          }}>
            {(alert.score_ensemble * 100).toFixed(1)}%
          </span>
          <span style={{
            fontSize: '11px', padding: '2px 8px', borderRadius: '12px',
            background: alert.status === 'CONTAINED' ? '#E8F5E9' : '#FFF3E0',
            color: alert.status === 'CONTAINED' ? '#2E7D32' : '#E65100',
            fontWeight: 700,
          }}>
            {alert.status}
          </span>
        </div>
      ))}

      {alerts.length === 0 && (
        <div style={{
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          height: '200px', color: '#78909C', fontFamily: 'Calibri, sans-serif',
          fontSize: '14px',
        }}>
          ✓ No alerts — all zones normal
        </div>
      )}
    </div>
  );
};
