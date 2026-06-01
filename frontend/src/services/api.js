const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:4000';

const request = async (path, options = {}) => {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.message || `Request failed with status ${response.status}`);
  }

  return response.json();
};

export const fetchFootballTrends = () => request('/api/football-trends');
export const fetchTrendingContent = () => request('/api/trending-content');
export const fetchSavedScripts = () => request('/api/scripts');

export const generateScript = (payload) =>
  request('/api/script-generator', {
    method: 'POST',
    body: JSON.stringify(payload),
  });

export const saveScript = (payload) =>
  request('/api/scripts', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
