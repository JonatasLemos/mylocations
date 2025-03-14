import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import RegistrationForm from './components/register_form';
import LocationType from './components/location_types_list';
import UserLocation from './components/user_locations_table';
import LoginForm from './components/login_form';
import Logout from './components/logout_button';
import CreateLocationForm from './components/create_location_form';

const Navbar = () => {
  const isLoggedIn = !!sessionStorage.getItem('access_token'); 
  const location = useLocation(); 

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary px-4">
      <Link to="/" className="navbar-brand">MyLocations</Link>
      
      <button 
        className="navbar-toggler" 
        type="button" 
        data-bs-toggle="collapse" 
        data-bs-target="#navbarNav"
      >
        <span className="navbar-toggler-icon"></span>
      </button>

      <div className="collapse navbar-collapse" id="navbarNav">
        <ul className="navbar-nav me-auto">
          {!isLoggedIn && (
            <li className={`nav-item ${location.pathname === "/registration" ? "active" : ""}`}>
              <Link to="/registration" className="nav-link">Register</Link>
            </li>
          )}
          {isLoggedIn && (
            <>
              <li className={`nav-item ${location.pathname === "/add-location" ? "active" : ""}`}>
                <Link to="/add-location" className="nav-link">Add new location</Link>
              </li>
              <li className={`nav-item ${location.pathname === "/my-locations" ? "active" : ""}`}>
                <Link to="/my-locations" className="nav-link">See my locations</Link>
              </li>
              <li className={`nav-item ${location.pathname === "/location" ? "active" : ""}`}>
                <Link to="/location" className="nav-link">Location Types</Link>
              </li>
            </>
          )}
        </ul>
        <div className="d-flex">
          {isLoggedIn ? <Logout /> : <Link to="/" className="btn btn-outline-light">Login</Link>}
        </div>
      </div>
    </nav>
  );
};

function App() {
  return (
    <Router>
      <div className="container-fluid p-0">
        <Navbar />
        <div className="container mt-4">
          <Routes>
            <Route path="/registration" element={<RegistrationForm />} />
            <Route path="/" element={<LoginForm />} />
            <Route path="/location" element={<LocationType />} />
            <Route path="/my-locations" element={<UserLocation />} />
            <Route path="/add-location" element={<CreateLocationForm />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
