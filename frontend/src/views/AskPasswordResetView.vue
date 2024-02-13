<template>
  <v-container
    class="d-flex flex-column pt-sm-8 pt-2"
    style="width: 100%; max-width: 500px; gap: 16px">
    <h1 class="text-h2 text-center">Password reset</h1>
    <v-form
      v-model="valid"
      validate-on="input"
      class="d-flex flex-column justify-center align-content-center mt-4"
      style="gap: 16px"
      @submit.prevent="resetPassword">
      <v-text-field
        v-model="email"
        :rules="emailRules"
        hide-details="auto"
        label="Email"
        required></v-text-field>
      <v-btn
        :disabled="!valid || loading"
        :loading="loading"
        color="primary"
        type="submit">
        Reset password
      </v-btn>
    </v-form>
  </v-container>
</template>

<script>
import rules from "@/services/rules.js";

export default {
  name: "AskForgotPasswordView",
  data() {
    return {
      valid: true,
      email: "",
      loading: false,
    };
  },
  computed: {
    emailRules() {
      return [rules.required("Email"), rules.email()];
    },
  },
  methods: {
    resetPassword() {
      this.loading = true;
      this.$store
        .dispatch("auth/askPasswordReset", {
          email: this.email,
        })
        .then(() => {
          this.$store.commit("snackbar/show", {
            message: "Password reset email sent",
            color: "success",
          });
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
