<template>
  <span v-if="loadingData"> Loading </span>
  <div v-else>
    <v-btn :loading="loading" :disabled="loading" variant="text">
      {{ activeCompany?.name }}
    </v-btn>
    <v-btn icon="mdi-swap-vertical"
           title="Switch Company"
           variant="text" id="company-menu-activator" density="comfortable"/>
    <v-menu
      offset-y
      location="bottom right"
      width="200"
      transition="scale-transition"
      activator="#company-menu-activator">
      <v-list>
        <v-list-item
          v-for="company in companies"
          :key="company.id"
          @click="switchCompany(company)">
          <v-list-item-title>{{ company.name }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </div>
</template>

<script>
export default {
  name: "CompanySwitcher",
  data() {
    return {
      loadingData: false,
      loading: false,
    };
  },
  computed: {
    companies() {
      return this.$store.getters["company/list"];
    },
    activeCompany() {
      return this.$store.getters["company/active"];
    },
  },
  created() {
    this.loadingData = true;
    this.$store.dispatch("company/fetchAll").finally(() => {
      this.loadingData = false;
    });
  },
  methods: {
    switchCompany(company) {
      this.loading = true;
      this.$store.dispatch("company/switchCompany", company.id).finally(() => {
        this.loading = false;
      });
    },
  },
};
</script>

<style scoped></style>
