import { fetchWithTokenRefresh } from './utils/fetch';

export const getLocationTypes = async (page = 1, size = 10, order = 'asc') => {
  const url = `http://localhost:8000/location-types/list/?page=${page}&size=${size}&order=${order}`;
  return fetchWithTokenRefresh(url, { method: 'GET' });
};

export const getUserLocations = async (page = 1, size = 10, order = 'asc') => {
  const url = `http://localhost:8000/my-locations/list/?page=${page}&size=${size}&order=${order}`;
  return fetchWithTokenRefresh(url, { method: 'GET' });
};