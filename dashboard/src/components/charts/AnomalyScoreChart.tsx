import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine } from 'recharts';

interface DataPoint {
  time: string;
  [zone: string]: number | string;
}

interface AnomalyScoreChartProps {
  data: DataPoint[];
  zones: string[];
}

const ZONE_COLORS = ['#00695C', '#FF8F00', '#00897B', '#C62828', '#2E7D32', '#E65100'];

export const AnomalyScoreChart: React.FC<AnomalyScoreChartProps> = ({ data, zones }) => {
  return (
    <div style={{ background: 'white', borderRadius: '8px', padding: '16px', boxShadow: '0 2px 8px rgba(0,0,0,0.08)' }}>
      <h3 style={{ fontFamily: 'Cambria, serif', color: '#004D40', margin: '0 0 16px 0', fontSize: '18px' }}>
        Anomaly Score Trend
      </h3>
      <LineChart width={600} height={300} data={data}
                 margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#ECEFF1" />
        <XAxis dataKey="time" tick={{ fontSize: 11, fill: '#78909C' }} />
        <YAxis domain={[0, 1]} tick={{ fontSize: 11, fill: '#78909C' }} />
        <Tooltip />
        <Legend />
        <ReferenceLine y={0.40} stroke="#C62828" strokeDasharray="5 5" label={{ value: 'Threshold 0.40', fontSize: 11 }} />
        <ReferenceLine y={0.70} stroke="#E65100" strokeDasharray="5 5" label={{ value: 'Threshold 0.70', fontSize: 11 }} />
        {zones.map((zone, i) => (
          <Line key={zone} type="monotone" dataKey={zone} stroke={ZONE_COLORS[i % ZONE_COLORS.length]}
                dot={false} strokeWidth={2} />
        ))}
      </LineChart>
    </div>
  );
};
