import axios from "axios";

export default axios.create({
  baseURL: `http://localhost:2455`,
});

// How to use base api

// const response = await API.get(`users/${USER_ID}`);

// console.log(response);
// console.log(response.data);
