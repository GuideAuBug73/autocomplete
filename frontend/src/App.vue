<script setup lang="ts">
import { RouterView } from 'vue-router'
import CitySearch from './components/CitySearch.vue'
</script>

<template>
  <main>
    <CitySearch />
  </main>
  <RouterView />
</template>

<style scoped>
main {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
}
</style>
