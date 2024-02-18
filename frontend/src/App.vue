<template>
  <v-app>
    <v-main>
      <MainNavbar/>
      <router-view :key="$route.fullPath"/>
    </v-main>
  </v-app>
</template>

<script>
import MainNavbar from "@/components/MainNavbar.vue";

export default {
  name: "App",
  components: {MainNavbar},
};
</script>
