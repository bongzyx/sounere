import logo from './logo.svg';
import './App.css';
import { useState, useEffect } from 'react';
import Home from './routes/Home';
import Login from './routes/Login';
import { Route, Routes } from "react-router-dom";
import RouteGuard from './routes/RouteGuard';
import AuthProvider, { AuthContext } from './context/AuthContext';
import { useContext } from 'react';
import NavBar from './routes/NavBar';
import Dashboard from './routes/Dashboard';
import Logout from './routes/Logout';
function App() {

  const ctx = useContext(AuthContext);

  return (
    <AuthProvider>
      <div className="App">
        <h1>sounere</h1>
        <NavBar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route exact path='/' element={<RouteGuard />}>
            <Route exact path='/dashboard' element={<Dashboard />} />
          </Route>
          <Route path="login" element={<Login />} />
          <Route path="logout" element={<Logout />} />

        </Routes>
      </div>
    </AuthProvider>
  );
}

export default App;
