import { create } from 'zustand';

interface Zone {
  zone_id: string;
  alert_level: 0 | 1 | 2 | 3;
  device_count: number;
  devices_monitored: number;
  devices_quarantined: number;
  active_alerts: number;
  last_update: string;
}

interface ShieldNetStore {
  zones: Record<string, Zone>;
  totalThreatsToday: number;
  totalContained: number;
  activeAlerts: number;
  totalDevices: number;
  globalModelVersion: string;
  lastFLRound: string;
  updateZone: (zone: Zone) => void;
  incrementThreats: () => void;
  setActiveAlerts: (count: number) => void;
  setModelVersion: (version: string) => void;
}

export const useShieldNetStore = create<ShieldNetStore>((set) => ({
  zones: {},
  totalThreatsToday: 0,
  totalContained: 0,
  activeAlerts: 0,
  totalDevices: 0,
  globalModelVersion: 'loading...',
  lastFLRound: '',

  updateZone: (zone) =>
    set((state) => ({
      zones: { ...state.zones, [zone.zone_id]: zone },
      totalDevices: Object.values({ ...state.zones, [zone.zone_id]: zone })
        .reduce((sum, z) => sum + z.device_count, 0),
      activeAlerts: Object.values({ ...state.zones, [zone.zone_id]: zone })
        .reduce((sum, z) => sum + z.active_alerts, 0),
    })),

  incrementThreats: () =>
    set((state) => ({ totalThreatsToday: state.totalThreatsToday + 1 })),

  setActiveAlerts: (count) => set({ activeAlerts: count }),
  setModelVersion: (version) => set({ globalModelVersion: version }),
}));
