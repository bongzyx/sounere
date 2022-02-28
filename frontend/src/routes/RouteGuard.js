import React, { useContext } from 'react'
import { Navigate, Outlet } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';


const RouteGuard = ({ component: Component, ...rest }) => {
  const auth = useContext(AuthContext);
  return (
    auth.verifyToken() ? <Outlet /> : <Navigate to="/login" />
  )
}

export default RouteGuard