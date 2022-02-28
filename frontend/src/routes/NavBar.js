import React, { useContext } from 'react'

import { NavLink } from 'react-router-dom'
import { AuthContext } from '../context/AuthContext'

const NavBar = () => {
  const ctx = useContext(AuthContext)
  return (
    <nav>
      <NavLink to="/">Home</NavLink>

      {ctx.verifyToken() ? <>
        <NavLink to="dashboard">Dashboard</NavLink>
        <NavLink to="logout">Logout</NavLink></>
        : <NavLink to="login">Login</NavLink>}
    </nav>
  )
}

export default NavBar