import React, { useState } from 'react';
import { registerUser } from '../api/login_api';

function RegistrationForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isSuccess, setSuccess] = useState(false); // Initial state should be false

  const handleSubmit = async (event) => {
    event.preventDefault();

    const { success, data } = await registerUser(username, password);

    if (success) {
      setMessage('Registration successful!');
      setSuccess(true);
    } else {
      setMessage('Cannot register user!');
      setSuccess(false);
    }
  };

  return (
    <div className="container mt-4 d-flex justify-content-center">
      <div className="col-md-6">
        <h2>Register</h2>
        <form onSubmit={handleSubmit} className="form-group">
          <div className="mb-3">
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="form-control"
            />
          </div>
          <div className="mb-3">
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="form-control"
            />
          </div>
          <button type="submit" className="btn btn-primary w-100">
            Register
          </button>
        </form>
        {message && isSuccess && (
          <div className="container mt-4 alert alert-success text-center" role="alert">
            {message}
          </div>
        )}
        {message && !isSuccess && (
          <div className="container mt-4 alert alert-danger text-center" role="alert">
            {message}
          </div>
        )}
      </div>
    </div>
  );
}

export default RegistrationForm;