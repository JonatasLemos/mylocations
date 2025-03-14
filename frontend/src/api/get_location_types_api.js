import { refreshAccessToken } from './refresh_token';


export const getLocationTypes = async (page = 1, size = 10, order = "asc") => {
    let token = sessionStorage.getItem("access_token");
    const refreshToken = sessionStorage.getItem("refresh_token");

    if (!token) {
        throw new Error("Not authenticated");
    }

    const fetchWithAuth = async (tokenToUse) => {
        const response = await fetch(`http://localhost:8000/location-types/list/?page=${page}&size=${size}&order=${order}`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${tokenToUse}`,
                "Content-Type": "application/json",
            },
        });

        if (response.ok) {
            return response.json();
        } else if (response.status === 401 && refreshToken) {
            // Token expired, attempt to refresh
            const newToken = await refreshAccessToken(refreshToken);
            if (newToken) {
                sessionStorage.setItem("access_token", newToken);
                return fetchWithAuth(newToken); // Retry the original request
            }
        }

        throw new Error("Failed to fetch location types");
    };

    return fetchWithAuth(token);
};
