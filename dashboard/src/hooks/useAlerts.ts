import { useState, useEffect } from 'react';

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

export const useAlerts = () => {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('/api/v1/threats?limit=50')
      .then(res => res.json())
      .then(data => {
        setAlerts(data.results || []);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return { alerts, loading, error };
};
