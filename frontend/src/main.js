import { createApp } from "vue";
import App from "./App.vue";
import router from "@/router/index.js";
import store from "@/store/index.js";
import vuetify from "@/plugins/vuetify.js";
import axios from "@/plugins/axios.js";

const app = createApp(App);
app.use(router);
app.use(store);
app.use(vuetify);
app.use(axios, { baseURL: "http://localhost:8000" });
app.mount("#app");
