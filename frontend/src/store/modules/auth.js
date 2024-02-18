export default {
  namespaced: true,
  state() {
    return {
      me: null,
    };
  },
  getters: {
    me(state) {
      return state.me;
    },
    isAuthenticated(state) {
      return !!state.me;
    },
  },
  mutations: {
    setMe(state, payload) {
      state.me = payload;
    },
  },
  actions: {
    checkAuth(context) {
      if (context.getters.isAuthenticated) {
        return Promise.resolve();
      }
      return this.$axios
        .get("/auth/me/")
        .then((response) => {
          context.commit("setMe", response.data);
        })
        .catch(() => {
          context.commit("setMe", null);
        });
    },
    login(context, payload) {
      return this.$axios.post("/auth/login/", payload).then((response) => {
        context.commit("setMe", response.data);
      });
    },
    askPasswordReset(context, payload) {
      return this.$axios.post("/auth/password-reset/", payload);
    },
    resetPassword(context, payload) {
      return this.$axios.post(
        `/auth/password-reset/${payload.token}/`,
        payload,
      );
    },
    logout(context) {
      return this.$axios.post("/auth/logout/").then(() => {
        context.commit("setMe", null);
      });
    },
    register(context, payload) {
      return this.$axios.post("/auth/register/", payload);
    },
  },
};
