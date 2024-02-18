<template>
  <v-app>
    <v-main>
      <MainNavbar />
      <router-view :key="$route.fullPath" />
      <SnackBar ref="snackbar" />
    </v-main>
  </v-app>
</template>

<script>
import MainNavbar from "@/components/MainNavbar.vue";
import SnackBar from "@/components/SnackBar.vue";

export default {
  name: "App",
  components: { SnackBar, MainNavbar },
};
</script>
