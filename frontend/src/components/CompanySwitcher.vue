<template>
  <span v-if="loadingData"> Loading </span>
  <div v-else-if="companies.length === 0">
    <v-btn
      :loading="loading"
      :disabled="loading"
      @click="()=>{}"
      variant="text">
      <template #prepend>
        <v-icon size="24" color="success">mdi-plus</v-icon>
      </template>
      <span style="margin-top:1px;">Create your first company</span>
    </v-btn>
  </div>
  <div v-else>
    <v-btn :loading="loading" :disabled="loading" variant="text">
      {{ activeCompany?.name }}
    </v-btn>
    <v-btn
      id="company-menu-activator"
      icon="mdi-swap-vertical"
      title="Switch Company"
      variant="text"
      density="comfortable" />
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
        <v-list-item v-if="companies.length === 0">
          <v-list-item-title>No companies found</v-list-item-title>
        </v-list-item>
        <v-divider class="my-1" />
        <v-list-item
          v-if="!loadingData"
          @click="()=>{}">
          <div class="d-flex flex-row" style="gap: 8px">
            <v-icon icon="mdi-plus" color="success" />
            <v-list-item-title>Create Company</v-list-item-title>
          </div>
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
