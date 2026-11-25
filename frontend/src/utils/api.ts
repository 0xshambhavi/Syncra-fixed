/// <reference types="vite/client" />
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export function getToken() { return localStorage.getItem('syncra_token'); }
export function setSession(token: string, user: any) {
  localStorage.setItem('syncra_token', token);
  localStorage.setItem('syncra_user', JSON.stringify(user));
}
export function clearSession() {
  localStorage.removeItem('syncra_token');
  localStorage.removeItem('syncra_user');
}
export function getStoredUser() {
  try { return JSON.parse(localStorage.getItem('syncra_user') || 'null'); } catch { return null; }
}
export async function api<T = any>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}), ...options.headers },
  });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.detail || body.message || `Request failed (${response.status})`);
  return body as T;
}
