<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="app-container">
    <header class="app-header">
      <h1 class="app-title">Recherche de Villes</h1>
      <p class="app-description">
        Trouvez facilement n'importe quelle ville en France et obtenez ses coordonnées géographiques
      </p>
    </header>
    <RouterView />
  </div>
</template>

<style scoped>
main {
  display: flex;
  justify-content: center;
  width: 100%;
}
</style>
