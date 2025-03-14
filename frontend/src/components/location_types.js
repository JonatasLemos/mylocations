import React, { useState } from 'react';
import { getLocationTypes} from '../api/get_location_types_api';

function LocationType() {
    const [locationTypes, setLocationTypes] = useState([]);
    const [error, setError] = useState(null);
    

    const handleFetchLocationTypes = async () => {
        try {
            setError(null);
            const data = await getLocationTypes();
            setLocationTypes(data.items || []);
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div className='container mt-4'>
            <button onClick={handleFetchLocationTypes} className="btn btn-primary mb-3">Load Location Types</button>

            {error && <p style={{ color: 'red' }}>{error}</p>}

            <ul className='list-group'>
                {locationTypes.map((type) => (
                    <li key={type.id} className='list-group-item'>{type.name}</li>
                ))}
            </ul>
        </div>
    );
}

export default LocationType;
