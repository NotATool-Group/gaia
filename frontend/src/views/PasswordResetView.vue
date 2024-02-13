<template>
  <v-container
    class="d-flex flex-column pt-sm-8 pt-2"
    style="width: 100%; max-width: 500px">
    <h1 class="text-h2 text-center">Password reset</h1>
    <v-form
      v-model="valid"
      validate-on="input"
      class="d-flex flex-column justify-center align-content-center mt-6"
      style="gap: 16px"
      @submit.prevent="resetPassword">
      <v-text-field
        v-model="password1"
        :rules="password1Rules"
        label="New password"
        type="password"
        hide-details="auto"
        required></v-text-field>
      <v-text-field
        v-model="password2"
        :rules="password2Rules"
        label="Confirm new password"
        type="password"
        :error-messages="password2Errors"
        hide-details="auto"
        required></v-text-field>
      <v-btn type="submit" :disabled="!valid" color="primary">
        Reset password
      </v-btn>
    </v-form>
  </v-container>
</template>

<script>
import rules from "@/services/rules.js";

export default {
  name: "ForgotPasswordView",
  data: () => ({
    password1: "",
    password2: "",
    password2Errors: [],
    valid: false,
    loading: false,
  }),
  computed: {
    password1Rules() {
      return [rules.required("Password"), rules.min_length(8, "Password")];
    },
    password2Rules() {
      return [
        rules.required("Password"),
        rules.min_length(8, "Password"),
        (value) => value === this.password1 || "Passwords do not match",
      ];
    },
  },
  methods: {
    resetPassword() {
      if (this.password1 !== this.password2) {
        this.password2Errors = ["Passwords do not match"];
        return;
      }
      this.loading = true;
      this.$store
        .dispatch("auth/resetPassword", {
          password: this.password1,
          token: this.$route.params.token,
        })
        .then(() => {
          this.$store.commit("snackbar/show", {
            message: "Password reset successfully",
            color: "success",
          });
          this.$router.push("/login");
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>

<style scoped></style>
