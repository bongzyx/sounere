import React, { createContext, useState, useEffect } from 'react'
import { useNavigate } from 'react-router';
import axios from '../utils/axios'
import jwt_decode from 'jwt-decode';

export const AuthContext = createContext({
  token: "",
  isLoggedIn: false,
  username: null,
  login: (params) => { },
  logout: () => { },
  verifyToken: () => { },
});

const AuthProvider = props => {
  const [token, setToken] = useState(null);
  const [refreshToken, setRefreshToken] = useState(null);
  var loginState = !!token;
  const navigate = useNavigate();

  const loginHandler = (params) => {
    setToken(params.access_token);
    setRefreshToken(params.refresh_token);
    localStorage.setItem(
      "tokens",
      JSON.stringify({
        access_token: params.access_token,
        refresh_token: params.refresh_token,
      })
    );
    console.log(localStorage.getItem("tokens"))
  };

  useEffect(() => {
    const storedData = JSON.parse(localStorage.getItem("tokens"));
    if (storedData) {
      if (storedData.access_token) {
        loginHandler({
          access_token: storedData.access_token,
          refresh_token: storedData.refresh_token,
        });
        // navigate("/dashboard");
        console.log("YPPPPPP")
      }
    }
  });

  const logoutHandler = () => {
    setRefreshToken(null);
    setToken(null);
    localStorage.removeItem("tokens");
  };

  const verifyToken = () => {
    var isExpired = false;
    const token = JSON.parse(localStorage.getItem("tokens"));
    if (!token) {
      return isExpired
    }
    const decodedToken = jwt_decode(token.access_token);
    const currentDate = new Date();

    // JWT exp is in seconds
    if (decodedToken.exp * 1000 < currentDate.getTime()) {
      console.log("Token expired.");
      return isExpired
    } else {
      console.log("Valid token");
      isExpired = true;
    }
    return isExpired
  };


  const contextValue = {
    token: token,
    isLoggedIn: loginState,
    username: "username",
    login: loginHandler,
    logout: logoutHandler,
    verifyToken: verifyToken,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {props.children}
    </AuthContext.Provider>
  )
};

export default AuthProvider;