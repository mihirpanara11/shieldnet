-- ShieldNet Supabase Schema
-- Run this in Supabase SQL Editor (https://supabase.com/dashboard/project/_/sql/new)

-- Incidents table
CREATE TABLE IF NOT EXISTS incidents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  incident_id TEXT UNIQUE NOT NULL,
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  zone_id TEXT NOT NULL,
  device_id TEXT DEFAULT '',
  device_category TEXT DEFAULT '',
  threat_class TEXT NOT NULL,
  confidence_score REAL DEFAULT 0.0,
  score_ensemble REAL DEFAULT 0.0,
  containment_time_ms INTEGER DEFAULT 0,
  status TEXT DEFAULT 'CONTAINED',
  playbook TEXT DEFAULT '',
  actions JSONB DEFAULT '[]',
  notes TEXT DEFAULT '',
  false_positive BOOLEAN DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_incidents_zone ON incidents(zone_id);
CREATE INDEX IF NOT EXISTS idx_incidents_status ON incidents(status);
CREATE INDEX IF NOT EXISTS idx_incidents_timestamp ON incidents(timestamp DESC);

-- Device profiles
CREATE TABLE IF NOT EXISTS device_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  device_id TEXT UNIQUE NOT NULL,
  zone_id TEXT NOT NULL,
  category TEXT NOT NULL,
  protocol TEXT DEFAULT 'MQTT',
  status TEXT DEFAULT 'online',
  firmware_version TEXT DEFAULT '',
  anomaly_score REAL DEFAULT 0.0,
  alerts_24h INTEGER DEFAULT 0,
  last_seen TIMESTAMPTZ DEFAULT NOW(),
  enrolled_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_devices_zone ON device_profiles(zone_id);
CREATE INDEX IF NOT EXISTS idx_devices_status ON device_profiles(status);

-- Zones
CREATE TABLE IF NOT EXISTS zones (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  zone_id TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  alert_level INTEGER DEFAULT 0,
  device_count INTEGER DEFAULT 0,
  active_alerts INTEGER DEFAULT 0,
  last_event TEXT DEFAULT '',
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Playbook executions
CREATE TABLE IF NOT EXISTS playbook_executions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  incident_id TEXT REFERENCES incidents(incident_id),
  playbook_id TEXT NOT NULL,
  status TEXT DEFAULT 'QUEUED',
  started_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  actions_taken JSONB DEFAULT '[]',
  error_message TEXT DEFAULT ''
);

-- FL rounds
CREATE TABLE IF NOT EXISTS fl_rounds (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  round_number INTEGER NOT NULL,
  global_model_version TEXT NOT NULL,
  participating_zones TEXT[] DEFAULT '{}',
  avg_loss REAL,
  avg_auc REAL,
  privacy_epsilon_consumed REAL DEFAULT 0.0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE incidents ENABLE ROW LEVEL SECURITY;
ALTER TABLE device_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE zones ENABLE ROW LEVEL SECURITY;

-- Public read-only access (safe for dashboard)
DROP POLICY IF EXISTS read_incidents ON incidents;
CREATE POLICY read_incidents ON incidents FOR SELECT USING (true);
DROP POLICY IF EXISTS read_devices ON device_profiles;
CREATE POLICY read_devices ON device_profiles FOR SELECT USING (true);
DROP POLICY IF EXISTS read_zones ON zones;
CREATE POLICY read_zones ON zones FOR SELECT USING (true);

-- Create API views for the dashboard
CREATE OR REPLACE VIEW active_alerts AS
  SELECT * FROM incidents ORDER BY timestamp DESC LIMIT 10;

CREATE OR REPLACE VIEW zone_summary AS
  SELECT
    zone_id,
    COUNT(*) as total_devices,
    SUM(CASE WHEN status = 'online' THEN 1 ELSE 0 END) as online,
    SUM(CASE WHEN status = 'degraded' THEN 1 ELSE 0 END) as degraded,
    SUM(CASE WHEN status = 'offline' THEN 1 ELSE 0 END) as offline,
    SUM(CASE WHEN status = 'quarantined' THEN 1 ELSE 0 END) as quarantined
  FROM device_profiles GROUP BY zone_id;
