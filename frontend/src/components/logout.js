import React from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate

function Logout() {
  const navigate = useNavigate(); // Initialize useNavigate

  const logout = () => {
    sessionStorage.removeItem('access_token');
    sessionStorage.removeItem('refresh_token');
    navigate('/'); // Use navigate to redirect
  };

  return (
    <button className="btn btn-danger btn-sm" onClick={logout}>
      Logout
    </button>
  );
}

export default Logout;