import { loadingPromise } from "@/store/utils";

export default {
  namespaced: true,
  state() {
    return {
      companies: [],
      active_company: null,
      loading: false,
    };
  },
  getters: {
    companies(state) {
      return state.companies;
    },
    activeCompany(state) {
      return state.active_company;
    },
    isLoading(state) {
      return state.loading;
    },
  },
  mutations: {
    setCompanies(state, payload) {
      state.companies = payload;
    },
    setActiveCompany(state, payload) {
      state.active_company = payload;
    },
    setLoading(state, payload) {
      state.loading = payload;
    },
  },
  actions: {
    fetchCompanies(context) {
      return loadingPromise(context, () => {
        return this.$axios.get("/companies/").then((response) => {
          context.commit("setCompanies", response.data);
        });
      });
    },
    fetchActiveCompany(context) {
      return loadingPromise(context, () => {
        return this.$axios.get(`/companies/active/`).then((response) => {
          context.commit("setActiveCompany", response.data);
        });
      });
    },
    switchCompany(context, payload) {
      return loadingPromise(context, () => {
        return this.$axios
          .post(`/companies/switch/`, payload)
          .then((response) => {
            context.commit("setActiveCompany", response.data);
          });
      });
    },
  },
};
