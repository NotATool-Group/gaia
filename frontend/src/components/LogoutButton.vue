<template>
  <v-btn :loading="loading" v-bind="$attrs" @click="logout"> Logout </v-btn>
</template>

<script>
export default {
  name: "LogoutButton",
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
