import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import RegistrationForm from './components/register';
import LocationType from './components/location_types';
import LoginForm from './components/login';
import Logout from './components/logout';

function App() {
  const isLoggedIn = !!sessionStorage.getItem('access_token'); 
  console.log(isLoggedIn,"hein")
  return (
    <Router>
      <div className="container mt-4">
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
          <ul className="navbar-nav mr-auto">
            <li className="nav-item">
              <Link to="/registration" className="nav-link">Register</Link>
            </li>
            <li className="nav-item">
              <Link to="/location" className="nav-link">Available locations</Link>
            </li>
          </ul>
          <div  className="ms-auto">
            <Logout/>
          </div> 
        </nav>
        <Routes>
          <Route path="/registration" element={<RegistrationForm />} />
          <Route path="/" element={<LoginForm />} />
          <Route path="/location" element={<LocationType />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;