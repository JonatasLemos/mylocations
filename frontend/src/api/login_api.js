export const registerUser = async (username, password) => {
  try {
    const response = await fetch("http://localhost:8000/users/register/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    const data = await response.json();
    return { success: response.ok, data };
  } catch (error) {
    console.error("Registration error:", error);
    return { success: false, data: { detail: "An unexpected error occurred" } };
  }
};

export const loginUser = async (username, password) => {
  try {
    const response = await fetch("http://localhost:8000/users/auth/token/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    const data = await response.json();
    return { success: response.ok, data };
  } catch (error) {
    console.error("Login error:", error);
    return { success: false, data: { detail: "An unexpected error occurred" } };
  }
};

export async function fetchUsername() {
  const accessToken = sessionStorage.getItem("access_token");

  if (!accessToken) {
    return { success: false, data: { detail: "Access token not found" } };
  }

  try {
    const response = await fetch("/users/me/", {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    if (!response.ok) {
      return { success: false, data: { detail: "Failed to fetch username" } };
    }

    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    console.error("Error fetching username:", error);
    return { success: false, data: { detail: "Network error" } };
  }
}
