import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import RegistrationForm from './components/login';
import LocationType from './components/location_types';

function App() {
  return (
    <Router>
      <div className="App">
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/location_type">Location Type</Link>
            </li>
          </ul>
        </nav>
        <Routes>
          <Route path="/" element={<RegistrationForm />} />
          <Route path="/location_type" element={<LocationType />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;