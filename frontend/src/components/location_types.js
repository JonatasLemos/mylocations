import React, { useState, useEffect } from "react";
import { getLocationTypes } from "../api/list_apis";
import UnauthenticatedMessage from "./unauthenticated_message";

function LocationType() {
  const [locations, setLocations] = useState([]);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = sessionStorage.getItem("access_token");
    if (token) {
      setIsAuthenticated(true);
      getLocationTypes()
        .then((data) => setLocations(data.items))
        .catch((err) => {
          setError(err.message);
          console.error("Error fetching location types:", err);
          setTimeout(() => {
            setError(null);
          }, 3000);
        });
    }
  }, []);

  if (!isAuthenticated) {
    return <UnauthenticatedMessage />;
  }

  return (
    <div className="container mt-4">
      <h2>User Locations</h2>

      {error && <div className="alert alert-danger">{error}</div>}

      {locations.length > 0 && (
        <ul className="list-group">
          {locations.map((location) => (
            <li key={location.id} className="list-group-item">
              {location.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default LocationType;
