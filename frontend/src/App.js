import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import RegistrationForm from './components/register';
import LocationType from './components/location_types';
import LoginForm from './components/login';

function App() {
  return (
    <Router>
      <div className="container mt-4">
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
          <ul className="navbar-nav mr-auto">
            <li className="nav-item">
              <Link to="/registration" className="nav-link">Register</Link>
            </li>
            <li className="nav-item">
              <Link to="/login" className="nav-link">Login</Link>
            </li>
            <li className="nav-item">
              <Link to="/location_type" className="nav-link">Available locations</Link>
            </li>
          </ul>
        </nav>
        <Routes>
          <Route path="/registration" element={<RegistrationForm />} />
          <Route path="/login" element={<LoginForm />} />
          <Route path="/location_type" element={<LocationType />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;