<template>
  <main>
    <h1>Recherche de Villes</h1>
    <CitySearch />
  </main>
</template>

<script setup lang="ts">
import CitySearch from '@/components/CitySearch.vue'
</script>

<style scoped>
main {
  padding: 20px;
  text-align: center;
}

h1 {
  margin-bottom: 30px;
  color: #2c3e50;
}
</style>
