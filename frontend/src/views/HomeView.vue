<template>
  <div class="home-view">
    <CitySearch />
  </div>
</template>

<script setup lang="ts">
import CitySearch from '@/components/CitySearch.vue'
</script>

<style scoped>
.home-view {
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 1rem;
}
</style>
