import {createApp} from 'vue'
import App from './App.vue'
import router from "@/router/index.js";
import store from "@/store/index.js";
import vuetify from "@/plugins/vuetify.js";

const app = createApp(App);
app.use(router);
app.use(store);
app.use(vuetify);
app.mount('#app');
