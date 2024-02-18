<template>
  <div>
    <h1>Ciao {{ me.first_name }} {{ me.last_name }}</h1>
  </div>
</template>

<script>
export default {
  name: "ProfileView",
  computed: {
    me() {
      return this.$store.getters["auth/me"];
    },
  },
};
</script>

<style scoped></style>
