import { refreshAccessToken } from './refresh_token';

export const fetchWithTokenRefresh = async (url, options = {}) => {
  let token = sessionStorage.getItem('access_token');
  const refreshToken = sessionStorage.getItem('refresh_token');

  if (!token) {
    console.warn('User is not authenticated');
    return { error: 'User is not authenticated' };
  }

  const fetchWithAuth = async (tokenToUse) => {
    const response = await fetch(url, {
      ...options,
      headers: {
        ...options.headers,
        Authorization: `Bearer ${tokenToUse}`,
        'Content-Type': 'application/json',
      },
    });

    if (response.ok) {
      return response.json();
    } else if (response.status === 401 && refreshToken) {
      console.log("hey")
      const newToken = await refreshAccessToken(refreshToken);
      console.log("billl")
      if (newToken) {
        sessionStorage.setItem('access_token', newToken);
        return fetchWithAuth(newToken);
      }
    }

    throw new Error('Failed to fetch data');
  };

  return fetchWithAuth(token);
};