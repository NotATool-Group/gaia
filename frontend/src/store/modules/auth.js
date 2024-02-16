import { loadingPromise } from "@/store/utils";

export default {
  namespaced: true,
  state() {
    return {
      me: null,
      loading: false,
    };
  },
  getters: {
    me(state) {
      return state.me;
    },
    isAuthenticated(state) {
      return !!state.me;
    },
    isLoading(state) {
      return state.loading;
    },
  },
  mutations: {
    setMe(state, payload) {
      state.me = payload;
    },
    setLoading(state, payload) {
      state.loading = payload;
    },
  },
  actions: {
    checkAuth(context) {
      if (context.getters.isAuthenticated) {
        return Promise.resolve();
      }
      return loadingPromise(context, () =>
        this.$axios
          .get("/auth/me/")
          .then((response) => {
            context.commit("setMe", response.data);
          })
          .catch(() => {
            context.commit("setMe", null);
          }),
      );
    },
    login(context, payload) {
      return loadingPromise(context, () =>
        this.$axios.post("/auth/login/", payload).then((response) => {
          context.commit("setMe", response.data);
        }),
      );
    },
    askPasswordReset(context, payload) {
      return loadingPromise(context, () =>
        this.$axios.post("/auth/password-reset/", payload),
      );
    },
    resetPassword(context, payload) {
      return loadingPromise(context, () =>
        this.$axios.post(`/auth/password-reset/${payload.token}/`, payload),
      );
    },
    logout(context) {
      return loadingPromise(context, () =>
        this.$axios.post("/auth/logout/").then(() => {
          context.commit("setMe", null);
        }),
      );
    },
    register(context, payload) {
      return loadingPromise(context, () =>
        this.$axios.post("/auth/register/", payload),
      );
    },
  },
};
