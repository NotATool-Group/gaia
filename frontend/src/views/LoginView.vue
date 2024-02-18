<template>
  <v-form v-model="valid" validate-on="input">
    <v-container
      class="d-flex flex-column pt-sm-8 pt-2"
      style="width: 100%; max-width: 500px; gap: 16px">
      <h1 class="text-h2 text-center">Login</h1>
      <v-text-field
        v-model="email"
        :error="formErrors.length > 0"
        :rules="emailRules"
        class="pt-4"
        hide-details="auto"
        label="Email"
        required
        validate-on="blur"
        @input="formErrors = []"></v-text-field>
      <v-text-field
        v-model="password"
        :error-messages="formErrors"
        :rules="passwordRules"
        hide-details="auto"
        label="Password"
        required
        type="password"
        @input="formErrors = []"></v-text-field>
      <v-btn
        id="login"
        :disabled="!valid || loading"
        :loading="loading"
        color="primary"
        @click="login">
        Login
      </v-btn>
    </v-container>
  </v-form>
</template>
<script>
export default {
  name: "LoginView",
  data() {
    return {
      valid: true,
      email: "",
      password: "",
      loading: false,
      formErrors: [],
    };
  },
  computed: {
    emailRules() {
      return [
        (v) => !!v || "E-mail is required",
        (v) => /.+@.+\..+/.test(v) || "E-mail must be valid",
      ];
    },
    passwordRules() {
      return [
        (v) => !!v || "Password is required",
        (v) => v.length >= 8 || "Password must be at least 8 characters",
      ];
    },
  },
  methods: {
    login() {
      if (!this.valid) {
        return;
      }
      this.loading = true;
      this.$store
        .dispatch("auth/login", {
          email: this.email,
          password: this.password,
        })
        .then(() => {
          this.$router.push({ name: "profile" });
        })
        .catch((error) => {
          if (error.response.status === 401) {
            this.formErrors = ["Invalid email or password"];
          } else {
            this.formErrors = ["An error occurred"];
          }
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>

<style scoped></style>
