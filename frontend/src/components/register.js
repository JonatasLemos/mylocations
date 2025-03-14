import React, { useState } from 'react';
import { registerUser } from '../api/login_api';

function RegistrationForm() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();

        const { success, data } = await registerUser(username, password);

        if (success) {
            setMessage("Registration successful!");
        } else {
            alert(data.detail || 'Registration failed');
            setMessage('');
        }
    };

    return (
    <div className="container mt-4 d-flex justify-content-center"> {/* Center the form */}
      <div className="col-md-6"> {/* Limit the form's width */}
        <h2>Register</h2>
        <form onSubmit={handleSubmit} className="form-group">
          <div className="mb-3"> {/* Margin bottom for the username input */}
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="form-control"
            />
          </div>
          <div className="mb-3"> {/* Margin bottom for the password input */}
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="form-control"
            />
          </div>
          <button type="submit" className="btn btn-primary">Register</button>
        </form>
        {message && <p className="mt-2">{message}</p>}
      </div>
    </div>
  );
}

export default RegistrationForm;
