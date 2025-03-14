import { fetchWithTokenRefresh } from "./utils/request";

export const getLocationTypes = async (page = 1, size = 10) => {
  const url = `http://localhost:8000/location-types/list/?page=${page}&size=${size}`;
  return fetchWithTokenRefresh(url, { method: "GET" });
};

export const getUserLocations = async (
  page = 1,
  size = 10,
  order_by = "user_location_id",
  order = "desc"
) => {
  const url = `http://localhost:8000/my-locations/list/?page=${page}&size=${size}&order_by=${order_by}&order=${order}`;
  return fetchWithTokenRefresh(url, { method: "GET" });
};
