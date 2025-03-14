export const refreshAccessToken = async (refreshToken) => {
    try {
        console.log("Attempting to refresh token...");
        const response = await fetch("http://localhost:8000/users/auth/refresh/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ refresh_token: refreshToken }),
        });

        const data = await response.json();

        if (response.ok) {
            console.log("Token refreshed successfully:", data.access_token);
            return data.access_token;
        } else {
            console.warn("Refresh token is invalid, logging out.");
            sessionStorage.removeItem("access_token");
            sessionStorage.removeItem("refresh_token");
            alert("Session expired. Please log in again.");
            window.location.href = "/"; // Redirect to login page
            return null;
        }
    } catch (error) {
        console.error("Error refreshing token:", error);
        return null;
    }
};
