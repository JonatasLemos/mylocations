import React, { useState } from 'react';
import { loginUser, fetchUsername} from '../api/login_api';
import { useNavigate } from 'react-router-dom'; // Import useNavigate

function LoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();

    const { success, data } = await loginUser(username, password);

    if (success) {
      sessionStorage.setItem('access_token', data.access_token);
      sessionStorage.setItem('refresh_token', data.refresh_token);
      setMessage('Login successful!');
      const usernameResponse = await fetchUsername();
      if(usernameResponse.success){
        alert(`Login successful! Welcome ${usernameResponse.data.username}`);
        setMessage(`Welcome ${usernameResponse.data.username}`);
        navigate('/my-locations');
      } else {
        alert(usernameResponse.data.detail || "Failed to fetch username");
        setMessage(usernameResponse.data.detail || "Failed to fetch username");
      }
    } else {
      alert(data.detail || 'Login failed');
      setMessage(data.detail || 'Login failed');
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
          <button type="submit" className="btn btn-primary w-100">Login</button>
        </form>
        {message && <p className="mt-2">{message}</p>}
      </div>
    </div>
  );
}

export default LoginForm;