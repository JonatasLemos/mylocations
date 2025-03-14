import React, { useState, useEffect } from 'react';
import { createLocation } from '../api/post_location';
import UnauthenticatedMessage from './unauthenticated_message';
import { useNavigate } from 'react-router-dom'; // Import useNavigate

function CreateLocationForm() {
  const [latitude, setLatitude] = useState(0);
  const [longitude, setLongitude] = useState(0);
  const [locationTypeId, setLocationTypeId] = useState(0);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [message, setMessage] = useState('');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [error, setError] = useState(null);
  const [isSuccess, setIsSuccess] = useState(false);
  const navigate = useNavigate(); // Initialize useNavigate

  useEffect(() => {
    const token = sessionStorage.getItem('access_token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();

    const locationData = {
      latitude: parseFloat(latitude),
      longitude: parseFloat(longitude),
      location_type_id: parseInt(locationTypeId),
      name,
      description,
    };

    try {
      setError(null);
      await createLocation(locationData);
      setMessage('Location created successfully!');
      setIsSuccess(true);
      setLatitude(0);
      setLongitude(0);
      setLocationTypeId(0);
      setName('');
      setDescription('');
      setTimeout(() => { // Add timeout and navigation
        navigate('/my-locations');
      }, 2000);
    } catch (err) {
      setError(err.message || 'An unknown error occurred.');
      setMessage('Failed to create location. Please try again.');
      setIsSuccess(false);
      console.error('Error creating location:', err);
    }
  };

  if (!isAuthenticated) {
    return <UnauthenticatedMessage />;
  }

  return (
    <div className="container mt-4 d-flex justify-content-center">
      <div className="w-50">
        <h3 className="mb-3">New Location</h3>
        <form onSubmit={handleSubmit} className="form-group">
          <div className="mb-3">
            <input
              type="number"
              placeholder="Latitude"
              onChange={(e) => setLatitude(e.target.value)}
              className="form-control"
            />
          </div>
          <div className="mb-3">
            <input
              type="number"
              placeholder="Longitude"
              onChange={(e) => setLongitude(e.target.value)}
              className="form-control"
            />
          </div>
          <div className="mb-3">
            <input
              type="number"
              placeholder="Location Type ID"
              onChange={(e) => setLocationTypeId(e.target.value)}
              className="form-control"
            />
          </div>
          <div className="mb-3">
            <input
              type="text"
              placeholder="Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="form-control"
            />
          </div>
          <div className="mb-3">
            <textarea
              placeholder="Description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="form-control"
            />
          </div>
          <button type="submit" className="btn btn-primary w-100">
            Create
          </button>
        </form>
        {message && isSuccess && (
          <div className="container mt-4 alert alert-success text-center" role="alert">
            {message}
          </div>
        )}
        {message && !isSuccess && (
          <div className="container mt-4 alert alert-danger text-center" role="alert">
            {error ? `${error}.` : message}
          </div>
        )}
      </div>
    </div>
  );
}

export default CreateLocationForm;