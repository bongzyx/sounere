import axios from "../utils/axios";
import React, { useContext, useState } from "react";

import AuthProvider, { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [enteredEmail, setEnteredEmail] = useState("");
  const [enteredPassword, setEnteredPassword] = useState("");

  const ctx = useContext(AuthContext);
  console.log(ctx)
  const history = useNavigate();

  const emailChangeHandler = (event) => {
    setEnteredEmail(event.target.value);
  };

  const passwordChangeHandler = (event) => {
    setEnteredPassword(event.target.value);
  };

  const onSubmitHandler = (event) => {
    event.preventDefault();
    setEnteredEmail("");
    setEnteredPassword("");
    sendData(enteredEmail, enteredPassword);
  };

  const sendData = async (username, password) => {
    const payload = {
      username,
      password,
    };
    try {
      const sendRequest = await axios({
        method: "post",
        url: "http://localhost:2455/auth/login",
        data: payload,
      });

      if (sendRequest.data.invalid) {
        console.log(sendRequest.data.response);
      } else {
        ctx.login(sendRequest.data);

        history("/dashboard");
      }

    } catch (error) {
      if (error) {
        console.error(error);
      }
    }
  };

  const checkToken = () => {

  }

  return (
    <div>
      <form onSubmit={onSubmitHandler}>
        <h2>Login</h2>
        <button onClick={checkToken}>check</button>
        <div >
          <label htmlFor="username">Username or Email</label>
          <input
            required
            type="text"
            id="username"
            value={enteredEmail}
            onChange={emailChangeHandler}
          />
        </div>
        {enteredEmail} {enteredPassword}
        <div >
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            onChange={passwordChangeHandler}
            required
            value={enteredPassword}
          />
        </div>

        <button type="submit">Login</button>
      </form>
    </div>

  );
};

export default Login;