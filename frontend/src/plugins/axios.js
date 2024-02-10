import axios from "axios";

export default (app, options) => {
  const instance = axios.create({
    baseURL: options.baseURL,
  });
  // set the X-CSRFToken header for all requests taking it from the cookie called csrftoken
  instance.defaults.xsrfCookieName = "csrftoken";
  instance.defaults.xsrfHeaderName = "X-CSRFToken";
  instance.defaults.withCredentials = true;
  app.config.globalProperties.$axios = instance;
};
