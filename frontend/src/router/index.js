import { createRouter, createWebHistory } from "vue-router";
import routes from "@/router/routes.js";

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
