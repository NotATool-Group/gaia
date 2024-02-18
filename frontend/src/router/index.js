import { createRouter, createWebHistory } from "vue-router";
import routes from "@/router/routes.js";
import store from "@/store";

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to) => {
  if (to.name === "login") return true;

  const requiresAuth = to.meta?.requiresAuth ?? false;
  await store.dispatch("auth/checkAuth");

  if (requiresAuth && !store.getters["auth/isAuthenticated"]) {
    return "/login";
  }

  return true;
});

export default router;
