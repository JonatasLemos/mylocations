import React from "react";
import { useNavigate } from "react-router-dom";

function Logout() {
  const navigate = useNavigate();

  const logout = () => {
    sessionStorage.removeItem("access_token");
    sessionStorage.removeItem("refresh_token");
    navigate("/");
  };

  return (
    <button className="btn btn-light btn-sm" onClick={logout}>
      Logout
    </button>
  );
}

export default Logout;
