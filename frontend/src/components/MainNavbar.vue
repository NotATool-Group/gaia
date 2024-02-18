<template>
  <v-app-bar app color="primary">
    <v-toolbar-title>
      <router-link class="text-decoration-none text-white" to="/">
        Gaia
      </router-link>
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn variant="text" @click="$router.push('/register')">Register</v-btn>
    <v-btn variant="text" @click="$router.push('/login')">Login</v-btn>
  </v-app-bar>
</template>

<script>
export default {
  name: "MainNavbar",
};
</script>

<style scoped></style>
