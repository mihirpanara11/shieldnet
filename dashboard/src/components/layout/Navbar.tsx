import React, { useState } from 'react';

const notifications = [
  { id: 1, text: 'DDoS detected in ZONE-04', time: '2m ago', severity: 'high' },
  { id: 2, text: 'Botnet beacon in ZONE-02', time: '15m ago', severity: 'medium' },
  { id: 3, text: 'Device CAM-0007 degraded', time: '1h ago', severity: 'low' },
];

const Navbar: React.FC = () => {
  const [showNotif, setShowNotif] = useState(false);

  return (
    <nav style={{
      background: '#004D40',
      color: 'white',
      padding: '0 24px',
      height: '56px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      fontFamily: 'Calibri, sans-serif',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <span style={{ fontWeight: 700, fontSize: '20px', fontFamily: 'Cambria, serif' }}>
          ShieldNet
        </span>
        <span style={{
          background: '#FF8F00',
          color: 'white',
          padding: '2px 8px',
          borderRadius: '4px',
          fontSize: '11px',
          fontWeight: 700,
          letterSpacing: '0.04em',
        }}>
          ALPHA401
        </span>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
        <select style={{
          background: 'transparent', color: 'white', border: '1px solid #4DD0C4',
          padding: '4px 8px', borderRadius: '4px', fontSize: '13px',
        }}>
          <option>ZONE-04</option>
          <option>ZONE-01</option>
          <option>ZONE-02</option>
          <option>ZONE-03</option>
        </select>
        <div style={{ position: 'relative' }}>
          <span
            style={{ position: 'relative', cursor: 'pointer', fontSize: '20px' }}
            onClick={() => setShowNotif(!showNotif)}
          >
            🔔
            <span style={{
              position: 'absolute', top: '-4px', right: '-10px',
              background: '#C62828', color: 'white', fontSize: '10px',
              borderRadius: '50%', padding: '1px 5px', fontWeight: 700,
            }}>{notifications.length}</span>
          </span>
          {showNotif && (
            <div style={{
              position: 'absolute', right: 0, top: '32px', width: '300px',
              background: 'white', color: '#333', borderRadius: '6px',
              boxShadow: '0 4px 16px rgba(0,0,0,0.2)', zIndex: 1000,
              fontFamily: 'Calibri, sans-serif',
            }}>
              <div style={{ padding: '10px 14px', borderBottom: '1px solid #eee', fontWeight: 700, fontSize: '13px' }}>
                Notifications
              </div>
              {notifications.map(n => (
                <div key={n.id} style={{
                  padding: '10px 14px', borderBottom: '1px solid #f5f5f5',
                  display: 'flex', alignItems: 'center', gap: '10px', fontSize: '13px',
                }}>
                  <span style={{
                    width: '8px', height: '8px', borderRadius: '50%', flexShrink: 0,
                    background: n.severity === 'high' ? '#C62828' : n.severity === 'medium' ? '#E65100' : '#FF8F00',
                  }} />
                  <div style={{ flex: 1 }}>
                    <div>{n.text}</div>
                    <div style={{ fontSize: '11px', color: '#999' }}>{n.time}</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
        <span style={{ cursor: 'pointer', fontSize: '13px' }}>Operator</span>
      </div>
    </nav>
  );
};

export default Navbar;
