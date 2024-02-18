import axios from "axios";

export default (app, options) => {
  const instance = axios.create({
    baseURL: options.baseURL,
  });
  instance.defaults.xsrfCookieName = "csrftoken";
  instance.defaults.xsrfHeaderName = "X-CSRFToken";
  instance.defaults.withCredentials = true;

  instance.interceptors.response.use(
    (response) => response,
    (error) => {
      const store = app.config.globalProperties.$store;
      if (
        error.response.status === 401 &&
        store.getters["auth/isAuthenticated"]
      ) {
        window.location.reload();
      }
      return Promise.reject(error);
    },
  );

  app.config.globalProperties.$axios = instance;
};
