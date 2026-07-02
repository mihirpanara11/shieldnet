import React from 'react';

const mockThreats = [
  { id: 'THR-001', type: 'DDoS', source: 'TRF-0042', zone: 'ZONE-04', score: 0.94, time: '2m ago', status: 'active' },
  { id: 'THR-002', type: 'Botnet', source: 'CAM-0012', zone: 'ZONE-02', score: 0.82, time: '15m ago', status: 'contained' },
  { id: 'THR-003', type: 'Unauthorized', source: 'ENR-0007', zone: 'ZONE-01', score: 0.71, time: '1h ago', status: 'contained' },
  { id: 'THR-004', type: 'Scanning', source: 'TRF-0089', zone: 'ZONE-04', score: 0.45, time: '2h ago', status: 'review' },
  { id: 'THR-005', type: 'MitM', source: 'CAM-0003', zone: 'ZONE-03', score: 0.91, time: '3h ago', status: 'contained' },
];

const statusStyles: Record<string, React.CSSProperties> = {
  active: { background: '#FFEBEE', color: '#C62828', padding: '2px 10px', borderRadius: '12px', fontWeight: 700, fontSize: '11px' },
  contained: { background: '#E8F5E9', color: '#2E7D32', padding: '2px 10px', borderRadius: '12px', fontWeight: 700, fontSize: '11px' },
  review: { background: '#FFF3E0', color: '#E65100', padding: '2px 10px', borderRadius: '12px', fontWeight: 700, fontSize: '11px' },
};

const Threats: React.FC = () => {
  return (
    <div style={{ fontFamily: 'Calibri, sans-serif' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1 style={{ fontFamily: 'Cambria, serif', color: '#004D40', margin: 0 }}>Threat Intelligence</h1>
        <div style={{ display: 'flex', gap: '8px' }}>
          <select style={{ padding: '8px 12px', border: '1px solid #CFD8DC', borderRadius: '4px', fontFamily: 'Calibri, sans-serif', fontSize: '13px' }}>
            <option>All Zones</option>
            <option>ZONE-01</option><option>ZONE-02</option><option>ZONE-03</option><option>ZONE-04</option>
          </select>
          <select style={{ padding: '8px 12px', border: '1px solid #CFD8DC', borderRadius: '4px', fontFamily: 'Calibri, sans-serif', fontSize: '13px' }}>
            <option>All Types</option>
            <option>DDoS</option><option>Botnet</option><option>Unauthorized</option><option>MitM</option><option>Scanning</option>
          </select>
        </div>
      </div>
      <div style={{ display: 'flex', gap: '16px', marginBottom: '24px' }}>
        {[{ label: 'Active Threats', value: 1, color: 'red' as const },
          { label: 'Contained Today', value: 12, color: 'teal' as const },
          { label: 'Avg Score', value: '0.766', color: 'amber' as const },
          { label: 'Response Time', value: '1.2s', color: 'teal600' as const }].map(k => (
          <div key={k.label} style={{
            flex: 1, borderTop: `4px solid ${k.color === 'red' ? '#C62828' : k.color === 'amber' ? '#FF8F00' : '#00695C'}`,
            background: k.color === 'red' ? '#FFEBEE' : '#E0F2F1', borderRadius: '8px', padding: '16px 20px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
          }}>
            <div style={{ fontSize: '36px', fontWeight: 700, fontFamily: 'Cambria, serif', color: k.color === 'red' ? '#B71C1C' : '#004D40' }}>{k.value}</div>
            <div style={{ fontSize: '12px', fontWeight: 700, color: '#37474F', textTransform: 'uppercase', letterSpacing: '0.04em', marginTop: '4px' }}>{k.label}</div>
          </div>
        ))}
      </div>
      <div style={{ background: 'white', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.08)', overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#004D40', color: 'white' }}>
              {['ID', 'Type', 'Source', 'Zone', 'Score', 'Detected', 'Status', 'Actions'].map(h => (
                <th key={h} style={{
                  padding: '12px 16px', textAlign: 'left', fontSize: '12px',
                  fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.04em',
                }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {mockThreats.map((t, i) => (
              <tr key={t.id} style={{ background: i % 2 === 0 ? '#E0F2F1' : 'white', borderBottom: '1px solid #ECEFF1' }}>
                <td style={{ padding: '10px 16px', fontSize: '12px', fontWeight: 700, color: '#004D40' }}>{t.id}</td>
                <td style={{ padding: '10px 16px', fontSize: '12px', fontWeight: 700, color: t.type === 'DDoS' || t.type === 'MitM' ? '#C62828' : '#E65100' }}>{t.type}</td>
                <td style={{ padding: '10px 16px', fontSize: '12px', fontFamily: 'Consolas, monospace', color: '#37474F' }}>{t.source}</td>
                <td style={{ padding: '10px 16px', fontSize: '12px', color: '#37474F' }}>{t.zone}</td>
                <td style={{ padding: '10px 16px', fontSize: '12px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <div style={{
                      width: '50px', height: '6px', background: '#ECEFF1', borderRadius: '3px', overflow: 'hidden',
                    }}>
                      <div style={{
                        width: `${t.score * 100}%`, height: '100%',
                        background: t.score >= 0.85 ? '#C62828' : t.score >= 0.70 ? '#E65100' : '#FF8F00',
                        borderRadius: '3px',
                      }} />
                    </div>
                    {(t.score * 100).toFixed(0)}%
                  </div>
                </td>
                <td style={{ padding: '10px 16px', fontSize: '12px', color: '#78909C' }}>{t.time}</td>
                <td style={{ padding: '10px 16px' }}>
                  <span style={statusStyles[t.status]}>{t.status}</span>
                </td>
                <td style={{ padding: '10px 16px' }}>
                  <button style={{ background: '#00695C', color: 'white', border: 'none', padding: '4px 12px', borderRadius: '4px', cursor: 'pointer', fontSize: '11px', fontWeight: 700 }}>Investigate</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Threats;
