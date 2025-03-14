import React from "react";
import { useNavigate } from "react-router-dom";

function UnauthenticatedMessage() {
  const navigate = useNavigate();
  const handleLoginClick = () => {
    navigate("/");
  };
  return (
    <div className="container mt-4">
      <div className="alert alert-warning text-center" role="alert">
        You are not authenticated. Please log in.
      </div>
      <button onClick={handleLoginClick} className="btn btn-primary mt-3">
        Login
      </button>
    </div>
  );
}

export default UnauthenticatedMessage;
