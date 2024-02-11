import { createStore } from "vuex";
import auth from "@/store/modules/auth.js";
import snackbar from "@/store/modules/snackbar.js";

export default createStore({
  state() {
    return {};
  },
  mutations: {},
  actions: {},
  modules: {
    auth,
    snackbar
  },
});
