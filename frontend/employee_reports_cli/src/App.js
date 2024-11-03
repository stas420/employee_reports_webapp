//import logo from './logo.svg';
import './App.css';
import React from 'react';
import { Navigate } from 'react-router-dom';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import User from './pages/user';
import Admin from './pages/admin';
import AdminPanel from './pages/adminPanel';
import { HelmetProvider } from 'react-helmet-async';

function App() {
  return (
    <HelmetProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Navigate to="/user"/>}/>
          <Route path="/user" element={<User />}/>
          <Route path="/admin" element={<Admin />}/>
          <Route path="/admin/panel" element={<AdminPanel />}/>
        </Routes>
      </Router>
    </HelmetProvider>
  );
}

export default App;

/*
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>

*/