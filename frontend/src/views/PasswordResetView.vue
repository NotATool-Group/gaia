<template>
  <v-container
    class="d-flex flex-column pt-sm-8 pt-2"
    style="width: 100%; max-width: 500px">
    <h1 class="text-h2 text-center">Password reset</h1>
    <v-form
      v-model="valid"
      class="d-flex flex-column justify-center align-content-center mt-6"
      style="gap: 16px"
      validate-on="input"
      @submit.prevent="resetPassword">
      <v-text-field
        v-model="password1"
        :error-messages="errors.password"
        :rules="password1Rules"
        hide-details="auto"
        label="New password"
        required
        type="password"
        @input="errors.password = []"></v-text-field>
      <v-text-field
        v-model="password2"
        :error-messages="password2Errors"
        :rules="password2Rules"
        hide-details="auto"
        label="Confirm new password"
        required
        type="password"></v-text-field>
      <v-btn
        :loading="loading"
        :disabled="!valid"
        color="primary"
        type="submit">
        Reset password
      </v-btn>
      <span v-if="errors.non_field_errors" class="text-red">
        {{ errors.non_field_errors[0] }}
      </span>
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
    errors: {},
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
        .catch((e) => {
          this.errors = e.response.data;
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>

<style scoped></style>
