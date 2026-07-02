import React, { useState } from 'react';

interface ConfigSection {
  title: string; fields: { label: string; key: string; type: string; desc: string }[];
}

const Settings: React.FC = () => {
  const [saved, setSaved] = useState(false);

  const [config, setConfig] = useState<Record<string, string>>({
    INFERENCE_THRESHOLD_LOW: '0.40',
    INFERENCE_THRESHOLD_HIGH: '0.70',
    DP_EPSILON: '1.0',
    DP_DELTA: '1e-5',
    DP_CLIP_NORM: '1.0',
    FL_LOCAL_EPOCHS: '3',
    FL_INTERVAL_MINUTES: '60',
    AIRO_CONFIRMATION_DELAY_MS: '5000',
    ALERT_WEBHOOK_URL: '',
    LOG_RETENTION_DAYS: '30',
    AUTO_CONTAIN_HIGH: 'true',
    AUTO_CONTAIN_MEDIUM: 'true',
    PROMETHEUS_SCRAPE_INTERVAL: '15s',
  });

  const sections: ConfigSection[] = [
    {
      title: 'Inference Engine',
      fields: [
        { label: 'Low Threshold', key: 'INFERENCE_THRESHOLD_LOW', type: 'number', desc: 'Scores below this are NORMAL' },
        { label: 'High Threshold', key: 'INFERENCE_THRESHOLD_HIGH', type: 'number', desc: 'Scores at or above this are THREAT_HIGH' },
      ],
    },
    {
      title: 'Differential Privacy',
      fields: [
        { label: 'Epsilon (ε)', key: 'DP_EPSILON', type: 'number', desc: 'Privacy budget per round (lower = more private)' },
        { label: 'Delta (δ)', key: 'DP_DELTA', type: 'text', desc: 'Probability of privacy leakage' },
        { label: 'Clip Norm', key: 'DP_CLIP_NORM', type: 'number', desc: 'Maximum gradient norm before clipping' },
      ],
    },
    {
      title: 'Federated Learning',
      fields: [
        { label: 'Local Epochs', key: 'FL_LOCAL_EPOCHS', type: 'number', desc: 'Training epochs per client per round' },
        { label: 'Interval (min)', key: 'FL_INTERVAL_MINUTES', type: 'number', desc: 'Minutes between FL rounds' },
      ],
    },
    {
      title: 'AIRO Response',
      fields: [
        { label: 'Confirmation Delay (ms)', key: 'AIRO_CONFIRMATION_DELAY_MS', type: 'number', desc: 'Wait window before auto-containment' },
      ],
    },
  ];

  const handleChange = (key: string, value: string) => {
    setConfig(prev => ({ ...prev, [key]: value }));
    setSaved(false);
  };

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div style={{ fontFamily: 'Calibri, sans-serif' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1 style={{ fontFamily: 'Cambria, serif', color: '#004D40', margin: 0 }}>System Settings</h1>
        <button onClick={handleSave} style={{
          background: saved ? '#2E7D32' : '#00695C', color: 'white', border: 'none',
          padding: '10px 24px', borderRadius: '4px', cursor: 'pointer', fontWeight: 700,
          fontFamily: 'Calibri, sans-serif', fontSize: '13px',
        }}>
          {saved ? 'Saved!' : 'Save Configuration'}
        </button>
      </div>
      {sections.map(section => (
        <div key={section.title} style={{ background: 'white', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.08)', padding: '24px', marginBottom: '16px' }}>
          <h3 style={{ fontFamily: 'Cambria, serif', color: '#004D40', margin: '0 0 16px 0', fontSize: '18px' }}>{section.title}</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '16px' }}>
            {section.fields.map(f => (
              <div key={f.key}>
                <label style={{ display: 'block', fontSize: '13px', fontWeight: 700, color: '#37474F', marginBottom: '4px' }}>{f.label}</label>
                <input
                  type={f.type}
                  value={config[f.key]}
                  onChange={e => handleChange(f.key, e.target.value)}
                  style={{
                    width: '100%', padding: '8px 12px', border: '1px solid #CFD8DC', borderRadius: '4px',
                    fontFamily: 'Consolas, monospace', fontSize: '13px', boxSizing: 'border-box',
                  }}
                />
                <div style={{ fontSize: '11px', color: '#78909C', marginTop: '4px' }}>{f.desc}</div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default Settings;
