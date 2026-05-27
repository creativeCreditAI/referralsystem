const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

async function request(path, options = {}) {
  const url = `${API_BASE_URL}${path}`;
  console.log(`[API] ${options.method || 'GET'} ${url}`);

  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });

  const text = await response.text();
  let data;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = text;
  }

  if (!response.ok) {
    const message = data?.detail || data?.message || 'Request failed';
    console.error(`[API] Error: ${message}`);
    throw new Error(message);
  }

  console.log(`[API] Success:`, data);
  return data;
}

export function createReferral(payload) {
  return request('/referral/', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function signupWithReferral(payload, ref) {
  const query = ref ? `?ref=${encodeURIComponent(ref)}` : '';
  return request(`/signup/${query}`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function getStats() {
  return request('/stats/', {
    method: 'GET',
  });
}
