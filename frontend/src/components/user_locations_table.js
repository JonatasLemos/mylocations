import React, { useState, useEffect } from "react";
import { getUserLocations } from "../api/fetch_locations";
import UnauthenticatedMessage from "./unauthenticated_alert";

const LocationsTable = () => {
  const [locations, setLocations] = useState([]);
  const [expanded, setExpanded] = useState({});
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = sessionStorage.getItem("access_token");
    if (token) {
      setIsAuthenticated(true);
      getUserLocations()
        .then((response) => {
          if (response.status === 404) {
            setError("You don't have locations yet.");
            setTimeout(() => {
              setError(null);
            }, 3000);
          } else {
            setLocations(response.items);
          }
        })
        .catch((err) => {
          setError(err.message);
          console.error("Error fetching user locations:", err);
          setTimeout(() => {
            setError(null);
          }, 3000);
        });
    }
  }, []);

  const toggleDetails = (id) => {
    setExpanded((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  if (!isAuthenticated) {
    return <UnauthenticatedMessage />;
  }

  return (
    <div className="container mt-4">
      <h3 className="mb-3">Available Locations</h3>
      {error && <div className="alert alert-danger">{error}</div>}{" "}
      <table className="table table-striped table-bordered">
        <thead className="thead-dark">
          <tr>
            <th>#</th>
            <th>Location Name</th>
            <th className="text-center">Actions</th>
          </tr>
        </thead>
        <tbody>
          {locations.map((location, index) => (
            <React.Fragment key={location.user_location_id}>
              <tr>
                <td>{index + 1}</td>
                <td>
                  <strong>{location.location_name}</strong>
                </td>
                <td className="text-center">
                  <button
                    className={`btn btn-${
                      expanded[location.user_location_id] ? "danger" : "primary"
                    } btn-sm`}
                    onClick={() => toggleDetails(location.user_location_id)}
                  >
                    {expanded[location.user_location_id]
                      ? "Hide Details"
                      : "Show Details"}
                  </button>
                </td>
              </tr>
              {expanded[location.user_location_id] && (
                <tr>
                  <td colSpan="3">
                    <div className="card p-3">
                      <p>
                        <strong>Description:</strong> {location.description}
                      </p>
                      <p>
                        <strong>Coordinates:</strong> Lat: {location.latitude},
                        Lng: {location.longitude}
                      </p>
                      <p>
                        <strong>Location Type:</strong>{" "}
                        {location.location_type_name}
                      </p>
                    </div>
                  </td>
                </tr>
              )}
            </React.Fragment>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default LocationsTable;
