import { fetchWithTokenRefresh } from './utils/fetch';

export const createLocation = async (locationData) => {
  try {
    const response = await fetchWithTokenRefresh(
      'http://localhost:8000/my-locations/create/',
      {
        method: 'POST',
        body: JSON.stringify(locationData),
      }
    );

    return response;
  } catch (error) {
    console.error('Error creating location:', error);
    throw error;
  }
};