import React from 'react';
import { KPIChip } from '../components/cards/KPIChip';
import { AlertFeed } from '../components/alerts/AlertFeed';
import { AnomalyScoreChart } from '../components/charts/AnomalyScoreChart';
import { ThreatHeatmap } from '../components/charts/ThreatHeatmap';
import { IncidentTable } from '../components/tables/IncidentTable';

const mockZones = [
  { zone_id: 'ZONE-01', alert_level: 0 as const, device_count: 342, active_alerts: 0, last_alert: '2h ago' },
  { zone_id: 'ZONE-02', alert_level: 1 as const, device_count: 287, active_alerts: 1, last_alert: '15m ago' },
  { zone_id: 'ZONE-03', alert_level: 0 as const, device_count: 156, active_alerts: 0, last_alert: '1h ago' },
  { zone_id: 'ZONE-04', alert_level: 2 as const, device_count: 398, active_alerts: 3, last_alert: '2m ago' },
  { zone_id: 'ZONE-05', alert_level: 0 as const, device_count: 211, active_alerts: 0, last_alert: '30m ago' },
];

const mockIncidents = [
  { incident_id: 'INC-2025-a3b4', timestamp_detected: '2025-01-15T08:32:11Z', zone_id: 'ZONE-04',
    device_category: 'traffic_sensor', threat_class: 'DDoS', score_ensemble: 0.923,
    containment_time_ms: 1459, status: 'CONTAINED' },
  { incident_id: 'INC-2025-c5d6', timestamp_detected: '2025-01-15T07:15:00Z', zone_id: 'ZONE-02',
    device_category: 'camera', threat_class: 'Scanning', score_ensemble: 0.451,
    containment_time_ms: 0, status: 'REVIEW' },
];

const Dashboard: React.FC = () => {
  return (
    <div style={{ fontFamily: 'Calibri, sans-serif' }}>
      <div style={{ display: 'flex', gap: '16px', marginBottom: '24px' }}>
        <KPIChip label="Threats Today" value={12} accentColor="teal" />
        <KPIChip label="Active Alerts" value={3} accentColor="amber" blinking />
        <KPIChip label="Auto-Contained" value={9} accentColor="teal600" />
        <KPIChip label="Devices Monitored" value={1394} accentColor="teal" />
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '24px' }}>
        <ThreatHeatmap zones={mockZones} />
        <AnomalyScoreChart data={[]} zones={['ZONE-04', 'ZONE-02']} />
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '24px' }}>
        <div>
          <h3 style={{ fontFamily: 'Cambria, serif', color: '#004D40', marginBottom: '12px', fontSize: '18px' }}>
            Live Alert Feed
          </h3>
          <AlertFeed />
        </div>
        <IncidentTable incidents={mockIncidents} />
      </div>
    </div>
  );
};

export default Dashboard;
