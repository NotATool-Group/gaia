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
    login(context, payload) {
      return this.$axios.post("/auth/login/", payload).then((response) => {
        context.commit("setMe", response.data);
      });
    },
    checkAuth(context) {
      if (context.getters.isAuthenticated) {
        return Promise.resolve();
      }
      return this.$axios.get("/auth/me/").then((response) => {
        context.commit("setMe", response.data);
      }).catch(() => {
        context.commit("setMe", null);
      });
    },
  },
};
