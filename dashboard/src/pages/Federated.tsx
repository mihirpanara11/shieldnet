import React from 'react';

const Federated: React.FC = () => {
  return (
    <div style={{ fontFamily: 'Calibri, sans-serif' }}>
      <h1 style={{ fontFamily: 'Cambria, serif', color: '#004D40', margin: '0 0 24px 0' }}>
        Federated Learning
      </h1>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
        <div style={{ background: 'white', borderRadius: '8px', padding: '20px', boxShadow: '0 2px 8px rgba(0,0,0,0.08)' }}>
          <div style={{ fontSize: '13px', color: '#78909C', textTransform: 'uppercase', letterSpacing: '0.04em' }}>Current Round</div>
          <div style={{ fontSize: '36px', fontWeight: 700, color: '#004D40', fontFamily: 'Cambria, serif' }}>47</div>
        </div>
        <div style={{ background: 'white', borderRadius: '8px', padding: '20px', boxShadow: '0 2px 8px rgba(0,0,0,0.08)' }}>
          <div style={{ fontSize: '13px', color: '#78909C', textTransform: 'uppercase', letterSpacing: '0.04em' }}>Global AUC-ROC</div>
          <div style={{ fontSize: '36px', fontWeight: 700, color: '#00695C', fontFamily: 'Cambria, serif' }}>0.974</div>
        </div>
        <div style={{ background: 'white', borderRadius: '8px', padding: '20px', boxShadow: '0 2px 8px rgba(0,0,0,0.08)' }}>
          <div style={{ fontSize: '13px', color: '#78909C', textTransform: 'uppercase', letterSpacing: '0.04em' }}>Participating Zones</div>
          <div style={{ fontSize: '36px', fontWeight: 700, color: '#00897B', fontFamily: 'Cambria, serif' }}>6</div>
        </div>
        <div style={{ background: 'white', borderRadius: '8px', padding: '20px', boxShadow: '0 2px 8px rgba(0,0,0,0.08)' }}>
          <div style={{ fontSize: '13px', color: '#78909C', textTransform: 'uppercase', letterSpacing: '0.04em' }}>Privacy Budget</div>
          <div style={{ fontSize: '36px', fontWeight: 700, color: '#FF8F00', fontFamily: 'Cambria, serif' }}>47/1000</div>
        </div>
      </div>
      <div style={{ background: 'white', borderRadius: '8px', padding: '24px', boxShadow: '0 2px 8px rgba(0,0,0,0.08)' }}>
        <h3 style={{ fontFamily: 'Cambria, serif', color: '#004D40', margin: '0 0 16px 0', fontSize: '18px' }}>
          Model Version History
        </h3>
        <p style={{ color: '#78909C', fontSize: '14px' }}>
          Current model: <strong style={{ color: '#004D40' }}>global-v47</strong>
          {' · '}Last aggregation: 2025-01-15 08:00:00 UTC
        </p>
      </div>
    </div>
  );
};

export default Federated;
