import { useEffect, useState } from 'react';
import { api, clearSession, getStoredUser, getToken } from './api';

export function useAuth() {
  const [user, setUser] = useState<any>(getStoredUser());
  const [loading, setLoading] = useState(Boolean(getToken()));
  useEffect(() => {
    if (!getToken()) { setLoading(false); return; }
    api('/api/v1/auth/me').then(setUser).catch(() => { clearSession(); setUser(null); }).finally(() => setLoading(false));
  }, []);
  return { user, loading, setUser, signOut: () => { clearSession(); setUser(null); } };
}
