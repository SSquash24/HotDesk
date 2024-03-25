import React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  NavLink,
} from "react-router-dom";
import ReactDOM from 'react-dom/client';
import './index.css';
import Profile from './Profile/Profile';
import Book from './Book/Book'
import Logout from './Logout/Logout'
import Login from './Login/Login'

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(

  <React.StrictMode>

    <Router>

      <nav className='navbar'>
        <NavLink to='/'>Profile</NavLink>
        <NavLink to='/book'>Book</NavLink>
        <NavLink to='/logout'>Logout</NavLink>
      </nav>

      <div className='main'>
        <Routes>
          <Route exact path="/" element={<Profile />} />
          <Route exact path="/book" element={<Book />} />
          <Route exact path="/logout" element={<Logout />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </div>
    </Router>
  </React.StrictMode>
);

