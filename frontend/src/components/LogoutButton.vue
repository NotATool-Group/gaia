<template>
  <v-btn
    v-if="icon"
    :loading="loading"
    icon="mdi-logout"
    v-bind="$attrs"
    @click="logout" />
  <v-btn v-else :loading="loading" v-bind="$attrs" @click="logout">
    Logout
  </v-btn>
</template>

<script>
export default {
  name: "LogoutButton",
  props: {
    icon: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      loading: false,
    };
  },
  methods: {
    logout() {
      this.loading = true;
      this.$store
        .dispatch("auth/logout")
        .then(() => {
          this.$router.push("/");
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>

<style scoped></style>
