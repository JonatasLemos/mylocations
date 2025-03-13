import React, { useState } from 'react';
import { registerUser,loginUser } from '../api/login_api';

function RegistrationForm() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();

        const { success, data } = await registerUser(username, password);

        if (success) {
            setMessage("Registration successful! Logging in...");
            
            const loginResponse = await loginUser(username, password);

            if (loginResponse.success) {
                sessionStorage.setItem('access_token', loginResponse.data.access); // Store token
                sessionStorage.setItem('refresh_token', loginResponse.data.refresh);
                alert('Login successful! Token stored.');
            } else {
                alert(loginResponse.data.detail || 'Login failed');
            }

            setUsername('');
            setPassword('');
        } else {
            alert(data.detail || 'Registration failed');
            setMessage('');
        }
    };

    return (
        <div>
            <h2>Register</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button type="submit">Register</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
}

export default RegistrationForm;
