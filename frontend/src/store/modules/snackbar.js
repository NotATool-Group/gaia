export default {
  namespaced: true,
  state() {
    return {
      message: "",
      icon: "",
      color: "",
      visible: false,
    };
  },
  getters: {
    message(state) {
      return state.message;
    },
    icon(state) {
      return state.icon;
    },
    color(state) {
      return state.color;
    },
    visible(state) {
      return state.visible;
    },
  },
  mutations: {
    show(state, { message, icon = "", color = "info" }) {
      state.message = message;
      state.icon = icon;
      state.color = color;
      state.visible = true;
    },
    setVisible(state, visible) {
      state.visible = visible;
    }
  },
};
