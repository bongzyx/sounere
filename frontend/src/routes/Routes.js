import React from "react";
import { Route, Routes as R } from "react-router-dom";
import Home from "./Home";
import Login from "./Login";


const Routes = () => (
  <R>
    <Route exact path="/" component={Home} />
    <Route path="/login" component={Login} />

  </R>
);

export default Routes;
