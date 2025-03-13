import React, { useState } from 'react';
import { registerUser } from '../api/login_api';

function RegistrationForm() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();

        // Save current state in case we need to restore it
        const prevUsername = username;
        const prevPassword = password;

        const { success, data } = await registerUser(username, password);

        if (success) {
            setMessage(data.message);
            setUsername('');
            setPassword('');
        } else {
            alert(data.detail || 'Registration failed');
            setMessage('');
            setUsername(prevUsername);
            setPassword(prevPassword);
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
