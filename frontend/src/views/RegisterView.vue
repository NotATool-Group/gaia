<template>
  <v-container class="pt-sm-8 pt-2" style="width: 100%; max-width: 500px">
    <h1 class="text-h2 text-center">Register</h1>
    <v-form
      v-if="showForm"
      v-model="valid"
      validate-on="input"
      class="d-flex flex-column mt-6"
      style="gap: 16px"
      @submit.prevent="register">
      <div class="d-flex flex-row align-start justify-start" style="gap: 16px">
        <v-text-field
          v-model="data.first_name"
          :rules="nameRules"
          :error-messages="errors.first_name"
          hide-details="auto"
          label="First Name"
          required
          validate-on="blur"
          @input="errors.first_name = []"></v-text-field>
        <v-text-field
          v-model="data.last_name"
          :rules="nameRules"
          :error-messages="errors.last_name"
          hide-details="auto"
          label="Last Name"
          required
          validate-on="blur"
          @input="errors.last_name = []"></v-text-field>
      </div>
      <v-text-field
        v-model="data.email"
        :rules="emailRules"
        :error-messages="errors.email"
        hide-details="auto"
        label="Email"
        required
        validate-on="blur"
        @input="errors.email = []"></v-text-field>
      <v-text-field
        v-model="data.password1"
        :rules="passwordRules"
        :error-messages="errors.password"
        hide-details="auto"
        label="Password"
        required
        type="password"
        @input="errors.password = []"></v-text-field>
      <v-text-field
        v-model="data.password2"
        :rules="repeatPasswordRules"
        :error-messages="errors.repeatPassword"
        hide-details="auto"
        label="Repeat password"
        required
        validate-on="input"
        type="password"
        @input="errors.repeatPassword = []"></v-text-field>
      <v-btn
        id="login"
        :disabled="!valid || loading"
        :loading="loading"
        type="submit"
        color="primary">
        Register
      </v-btn>
      <span v-if="errors.non_field_errors" class="text-red">
        {{ errors.non_field_errors[0] }}
      </span>
    </v-form>
    <p v-else class="text-center mt-2">
      An activation email has been sent to your email address.<br />
      Please click the link in the email to activate your account and be able to
      login.
    </p>
  </v-container>
</template>

<script>
import rules from "@/services/rules.js";

export default {
  name: "RegisterView",
  data() {
    return {
      valid: true,
      data: {
        first_name: "",
        last_name: "",
        email: "",
        password1: "",
        password2: "",
      },
      errors: {},
      showForm: true, // if false, show the activation email message
      loading: false,
    };
  },
  computed: {
    emailRules() {
      return [rules.required("Email"), rules.email()];
    },
    passwordRules() {
      return [rules.required("Password"), rules.min_length(8, "Password")];
    },
    repeatPasswordRules() {
      return [
        rules.required("Repeat password"),
        (value) => {
          if (value !== this.data.password1) {
            return "Passwords do not match";
          }
          return true;
        },
      ];
    },
    nameRules() {
      return [rules.required("Name")];
    },
  },
  watch: {
    "data.password1": function () {
      if (this.data.password1 === this.data.password2) {
        this.errors.repeatPassword = [];
      } else {
        this.errors.repeatPassword = ["Passwords do not match"];
      }
    },
  },
  methods: {
    register() {
      if (!this.valid) {
        return;
      }
      if (this.data.password1 !== this.data.password2) {
        this.errors.repeatPassword = ["Passwords do not match"];
        return;
      }
      this.loading = true;

      const registerData = {
        first_name: this.data.first_name,
        last_name: this.data.last_name,
        email: this.data.email,
        password: this.data.password1,
      };

      this.$store
        .dispatch("auth/register", registerData)
        .then(() => {
          this.showForm = false;
        })
        .catch((error) => {
          if (error.response.status === 400) {
            this.errors = error.response.data;
          } else {
            this.errors = { non_field_errors: ["An error occurred"] };
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
