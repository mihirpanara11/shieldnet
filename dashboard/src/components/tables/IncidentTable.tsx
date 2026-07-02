import React from 'react';

interface Incident {
  incident_id: string;
  timestamp_detected: string;
  zone_id: string;
  device_category: string;
  threat_class: string;
  score_ensemble: number;
  containment_time_ms: number;
  status: string;
}

interface IncidentTableProps {
  incidents: Incident[];
}

export const IncidentTable: React.FC<IncidentTableProps> = ({ incidents }) => {
  return (
    <div style={{ background: 'white', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.08)', overflow: 'hidden' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px' }}>
        <h3 style={{ fontFamily: 'Cambria, serif', color: '#004D40', margin: 0, fontSize: '18px' }}>
          Recent Incidents
        </h3>
        <button style={{
          background: '#00695C', color: 'white', border: 'none',
          padding: '8px 16px', borderRadius: '4px', cursor: 'pointer',
          fontFamily: 'Calibri, sans-serif', fontSize: '13px', fontWeight: 700,
        }}>
          Export CSV
        </button>
      </div>
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontFamily: 'Calibri, sans-serif' }}>
          <thead>
            <tr style={{ background: '#004D40', color: 'white' }}>
              {['ID', 'Time', 'Zone', 'Category', 'Type', 'Score', 'Containment', 'Status'].map(h => (
                <th key={h} style={{
                  padding: '12px 16px', textAlign: 'left', fontSize: '12px',
                  fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.04em',
                }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {incidents.map((inc, i) => (
              <tr key={inc.incident_id}
                  style={{ background: i % 2 === 0 ? '#E0F2F1' : 'white', borderBottom: '1px solid #ECEFF1' }}>
                <td style={{ padding: '10px 16px', fontSize: '12px', fontWeight: 700, color: '#004D40' }}>
                  {inc.incident_id}
                </td>
                <td style={{ padding: '10px 16px', fontSize: '12px', color: '#37474F' }}>
                  {new Date(inc.timestamp_detected).toLocaleString()}
                </td>
                <td style={{ padding: '10px 16px', fontSize: '12px', color: '#37474F' }}>{inc.zone_id}</td>
                <td style={{ padding: '10px 16px', fontSize: '12px', color: '#37474F' }}>
                  {inc.device_category.replace('_', ' ')}
                </td>
                <td style={{ padding: '10px 16px', fontSize: '12px', fontWeight: 700, color: inc.score_ensemble >= 0.85 ? '#C62828' : '#E65100' }}>
                  {inc.threat_class}
                </td>
                <td style={{ padding: '10px 16px', fontSize: '12px' }}>
                  {(inc.score_ensemble * 100).toFixed(1)}%
                </td>
                <td style={{ padding: '10px 16px', fontSize: '12px', color: '#37474F' }}>
                  {inc.containment_time_ms}ms
                </td>
                <td style={{ padding: '10px 16px', fontSize: '11px' }}>
                  <span style={{
                    padding: '2px 8px', borderRadius: '12px',
                    background: inc.status === 'CONTAINED' ? '#E8F5E9' : '#FFF3E0',
                    color: inc.status === 'CONTAINED' ? '#2E7D32' : '#E65100',
                    fontWeight: 700,
                  }}>
                    {inc.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {incidents.length === 0 && (
          <div style={{ textAlign: 'center', padding: '40px', color: '#78909C', fontSize: '14px' }}>
            No incidents recorded
          </div>
        )}
      </div>
    </div>
  );
};
