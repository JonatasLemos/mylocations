import React, { useState } from 'react';
import { loginUser, fetchUsername } from '../api/login_api';
import { useNavigate } from 'react-router-dom';

function LoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isSuccess, setIsSuccess] = useState(false); // Add isSuccess state
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();

    const { success, data } = await loginUser(username, password);

    if (success) {
      sessionStorage.setItem('access_token', data.access_token);
      sessionStorage.setItem('refresh_token', data.refresh_token);

      const usernameResponse = await fetchUsername();
      if (usernameResponse.success) {
        setMessage(`Welcome ${usernameResponse.data.username}`);
        setIsSuccess(true);
                setTimeout(() => {
          navigate('/my-locations');
        }, 2000); // 2000 milliseconds (2 seconds) delay
      } else {
        setMessage(usernameResponse.data.detail || 'Failed to fetch username');
        setIsSuccess(false);
      }
    } else {
      setMessage(data.detail || 'Login failed');
      setIsSuccess(false);
    }

    setUsername('');
    setPassword('');
  };

  return (
    <div className="container mt-4 d-flex justify-content-center">
      <div className="col-md-6">
        <h2>Login</h2>
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
            Login
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

export default LoginForm;