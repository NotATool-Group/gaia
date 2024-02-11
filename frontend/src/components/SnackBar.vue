<template>
  <v-snackbar
    v-model="visible"
    location="top right"
    timeout="5000"
    :color="color"
    transition="scale-transition">
    <v-icon v-if="icon">{{ icon }}</v-icon>
    {{ message }}
  </v-snackbar>
</template>

<script>
export default {
  name: "SnackBar",
  computed: {
    icon() {
      return this.$store.getters["snackbar/icon"];
    },
    message() {
      return this.$store.getters["snackbar/message"];
    },
    color() {
      return this.$store.getters["snackbar/color"];
    },
    visible: {
      get() {
        return this.$store.getters["snackbar/visible"];
      },
      set(value) {
        this.$store.commit("snackbar/setVisible", value);
      },
    },
  },
};
</script>

<style scoped></style>
