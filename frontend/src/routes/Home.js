import React, { useContext } from 'react'
import AuthProvider, { AuthContext } from "../context/AuthContext";

const Home = () => {
  const ctx = useContext(AuthContext);
  console.log(ctx)
  return (
    <div>Home</div>
  )
}

export default Home;