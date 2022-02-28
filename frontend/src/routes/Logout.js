import React, { useContext } from 'react'
import { useNavigate } from 'react-router';
import { AuthContext } from '../context/AuthContext';

const Logout = () => {
  const history = useNavigate();
  const ctx = useContext(AuthContext)
  ctx.logout()
  history("login")
  return (
    <div>Logout

    </div>
  )
}

export default Logout