export default {
  namespaced: true,
  state() {
    return {
      companies: [],
      active_company: null,
      loading: true,
      initialized: false,
    };
  },
  getters: {
    list(state) {
      return state.companies;
    },
    active(state) {
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
      return this.$axios.get("/company/").then((response) => {
        context.commit("setCompanies", response.data);
        console.log(response.data);
      });
    },
    fetchActiveCompany(context) {
      return this.$axios.get(`/company/active/`).then((response) => {
        context.commit("setActiveCompany", response.data);
      });
    },
    fetchAll(context) {
      if (context.state.initialized) return Promise.resolve();
      return Promise.all([
        context.dispatch("fetchCompanies"),
        context.dispatch("fetchActiveCompany"),
      ]).then(() => {
        context.state.initialized = true;
      });
    },
    switchCompany(context, company_id) {
      return this.$axios
        .post(`/company/switch/`, { company_id })
        .then((response) => {
          context.commit("setActiveCompany", response.data);
        });
    },
  },
};
