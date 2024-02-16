import { createStore } from "vuex";
import auth from "@/store/modules/auth.js";
import snackbar from "@/store/modules/snackbar.js";
import company from "@/store/modules/company.js";

export default createStore({
  state() {
    return {};
  },
  mutations: {},
  actions: {},
  modules: {
    auth,
    company,
    snackbar,
  },
});
