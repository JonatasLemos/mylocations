export const registerUser = async (username, password) => {
    try {
        const response = await fetch('http://localhost:8000/users/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        const data = await response.json();
        return { success: response.ok, data };

    } catch (error) {
        console.error('Registration error:', error);
        return { success: false, data: { detail: 'An unexpected error occurred' } };
    }
};

export const loginUser = async (username, password) => {
    try {
        const response = await fetch('http://localhost:8000/users/auth/token/', { // Update with your actual endpoint
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        const data = await response.json();
        return { success: response.ok, data };

    } catch (error) {
        console.error('Login error:', error);
        return { success: false, data: { detail: 'An unexpected error occurred' } };
    }
};
