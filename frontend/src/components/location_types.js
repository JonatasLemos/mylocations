import React, { useState } from 'react';
import { getLocationTypes} from '../api/list_apis';

function LocationType() {
    const [locationTypes, setLocationTypes] = useState([]);
    const [error, setError] = useState(null);
    const [isCollapsed, setIsCollapsed] = useState(false);
    

    const handleFetchLocationTypes = async () => {
        setIsCollapsed(!isCollapsed); // Toggle collapse
        if (isCollapsed || locationTypes.length > 0) return; // If already collapsed, don't fetch again
        try {
            setError(null);
            const data = await getLocationTypes();
            setLocationTypes(data.items || []);
        } catch (err) {
            setError(err.message);
        }
    };

    return (
    <div className="container mt-4">
      <div id="accordion">
        <div className="card">
          <div className="card-header" id="headingOne">
            <h5 className="mb-0">
              <button
                className="btn btn-light"
                onClick={handleFetchLocationTypes}
                aria-expanded={isCollapsed}
                aria-controls="collapseOne"
              >
                Location Types
              </button>
            </h5>
          </div>

          <div
            id="collapseOne"
            className={`collapse ${isCollapsed ? 'show' : ''}`}
            aria-labelledby="headingOne"
            data-parent="#accordion"
          >
            <div className="card-body">
              {error && <div className="alert alert-danger">{error}</div>}
              <ul className="list-group">
                {locationTypes.map((type) => (
                  <li key={type.id} className="list-group-item">
                    {type.id} - {type.name}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LocationType;
