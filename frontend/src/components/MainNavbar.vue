<template>
  <v-app-bar app color="primary">
    <v-toolbar-title>
      <router-link class="text-decoration-none text-white" to="/">
        Gaia
      </router-link>
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <template v-if="!authenticated">
      <v-btn variant="text" @click="$router.push('/register')">Register</v-btn>
      <v-btn variant="text" @click="$router.push('/login')">Login</v-btn>
    </template>
    <template v-else>
      <CompanySwitcher />
      <v-divider vertical class="mx-4" style="height: 50%; margin-top:auto; margin-bottom:auto" color="white"/>
      <v-btn variant="text" @click="$router.push('/profile')">
        <v-skeleton-loader
          :loading="$store.getters['auth/isLoading']"
          color="transparent"
          type="text"
          width="200">
          <template #default>
            <span>
              {{ $store.getters["auth/me"].first_name[0] }}.
              {{ $store.getters["auth/me"].last_name }}
            </span>
          </template>
        </v-skeleton-loader>
      </v-btn>
      <LogoutButton icon />
    </template>
  </v-app-bar>
</template>

<script>
import LogoutButton from "@/components/LogoutButton.vue";
import CompanySwitcher from "@/components/CompanySwitcher.vue";

export default {
  name: "MainNavbar",
  components: { CompanySwitcher, LogoutButton },
  computed: {
    authenticated() {
      return this.$store.getters["auth/isAuthenticated"];
    },
  },
};
</script>

<style scoped></style>
