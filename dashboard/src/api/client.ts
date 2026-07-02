const API_BASE = '/api/v1';

async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

export const api = {
  getHealth: () => request('/health'),
  getThreats: (params?: Record<string, string>) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    return request(`/threats${query}`);
  },
  getDevices: (params?: Record<string, string>) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    return request(`/devices${query}`);
  },
  getFLStatus: () => request('/federated/status'),
  reviewThreat: (incidentId: string, body: object) =>
    request(`/threats/${incidentId}/review`, {
      method: 'POST',
      body: JSON.stringify(body),
    }),
  airoOverride: (body: object) =>
    request('/airo/override', {
      method: 'POST',
      body: JSON.stringify(body),
    }),
};
