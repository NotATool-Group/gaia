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
      return this.$axios.get("/auth/me/").then((response) => {
        context.commit("setMe", response.data);
      });
    },
  },
};
