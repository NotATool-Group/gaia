import store from "@/store/index.js";

export default [
  {
    path: "/",
    name: "home",
    component: () => import("@/views/HomeView.vue"),
  },
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/LoginView.vue"),
  },
  {
    path: "/register",
    name: "register",
    component: () => import("@/views/RegisterView.vue"),
  },
  {
    path: "/activate/success",
    name: "activate-success",
    redirect: () => {
      store.commit("snackbar/show", {
        message: "Your account has been activated successfully",
        color: "success",
        icon: "mdi-check-circle",
      });
      return { name: "login" };
    },
  },
  {
    path: "/profile",
    name: "profile",
    meta: {
      requiresAuth: true,
    },
    component: () => import("@/views/ProfileView.vue"),
  },
];
