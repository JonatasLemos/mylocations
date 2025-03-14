import React, { useState } from 'react';
import { createLocation } from '../api/post_location';

function CreateLocationForm() {
  const [latitude, setLatitude] = useState(0);
  const [longitude, setLongitude] = useState(0);
  const [locationTypeId, setLocationTypeId] = useState(0);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [message, setMessage] = useState('');

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
      await createLocation(locationData); // Use the createLocation function
      setMessage('Location created successfully!');
      // Reset form fields if needed
      setLatitude(0);
      setLongitude(0);
      setLocationTypeId(0);
      setName('');
      setDescription('');
    } catch (error) {
      setMessage('Failed to create location. Please try again.');
      console.error('Error creating location:', error);
    }
  };

  return (
    <div className="container mt-4">
      <h3>New location</h3>
      <form onSubmit={handleSubmit} className="form-group">
        <div className="mb-3">
          <input
            type="number"
            placeholder="Latitude"
            value={latitude}
            onChange={(e) => setLatitude(e.target.value)}
            className="form-control"
          />
        </div>
        <div className="mb-3">
          <input
            type="number"
            placeholder="Longitude"
            value={longitude}
            onChange={(e) => setLongitude(e.target.value)}
            className="form-control"
          />
        </div>
        <div className="mb-3">
          <input
            type="number"
            placeholder="Location Type ID"
            value={locationTypeId}
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
        <button type="submit" className="btn btn-primary">
          Create
        </button>
      </form>
      {message && <p className="mt-2">{message}</p>}
    </div>
  );
}

export default CreateLocationForm;