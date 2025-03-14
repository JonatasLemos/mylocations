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
      const newToken = await refreshAccessToken(refreshToken);
      if (newToken) {
        sessionStorage.setItem('access_token', newToken);
        return fetchWithAuth(newToken);
      }
    }

    const errorDetails = {
      status: response.status,
      statusText: response.statusText,
      url: response.url,
      // You can add more details from the response object here
    };
    throw new Error(`Something went wrong. status: ${JSON.stringify(errorDetails.status)} msg: ${JSON.stringify(errorDetails.statusText)}`);
  };

  return fetchWithAuth(token);
};