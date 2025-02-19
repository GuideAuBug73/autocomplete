<!-- 
  Composant de recherche de villes avec autocomplétion
  Permet à l'utilisateur de :
  - Rechercher une ville en temps réel
  - Voir une liste de suggestions de villes avec leurs détails
  - Sélectionner une ville pour voir ses coordonnées
-->
<template>
  <div class="city-search">
    <div class="search-container">
      <input
        type="text"
        v-model="searchQuery"
        @input="handleInput"
        placeholder="Rechercher une ville..."
        class="search-input"
      />
      <ul v-if="cities.length > 0" class="city-list">
        <li
          v-for="city in cities"
          :key="`${city.name}-${city.lat}-${city.lon}`"
          @click="selectCity(city)"
          class="city-item"
        >
          <div class="city-item-name">{{ city.name }}</div>
          <div class="city-item-details">
            {{ [city.state, city.country].filter(Boolean).join(', ') }}
            <span v-if="city.county">({{ city.county }})</span>
          </div>
        </li>
      </ul>
    </div>

    <div v-if="selectedCity" class="city-details">
      <h2>{{ selectedCity.name }}</h2>
      <p v-if="selectedCity.state">Région: {{ selectedCity.state }}</p>
      <p v-if="selectedCity.county">Département: {{ selectedCity.county }}</p>
      <p>Pays: {{ selectedCity.country }}</p>
      <p>Latitude: {{ selectedCity.lat }}</p>
      <p>Longitude: {{ selectedCity.lon }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
// Import des fonctionnalités Vue nécessaires
import { ref, watch } from 'vue'  // ref pour la réactivité des données
import { debounce } from 'lodash' // Pour limiter les appels API pendant la saisie

// Interface définissant la structure d'une ville
interface City {
  name: string     // Nom de la ville
  country: string  // Pays
  state?: string   // État/Région (optionnel)
  county?: string  // Département/Comté (optionnel)
  lat: number      // Latitude
  lon: number      // Longitude
}

// Variables réactives pour stocker l'état du composant
const searchQuery = ref('')              // Texte saisi par l'utilisateur
const cities = ref<City[]>([])          // Liste des villes suggérées
const selectedCity = ref<City | null>(null)  // Ville sélectionnée

// Fonction pour récupérer les suggestions de villes depuis l'API
const fetchCities = async (query: string) => {
  // Ne fait pas de requête si la recherche est trop courte
  if (query.length < 2) {
    cities.value = []
    return
  }

  try {
    // Récupère la langue du navigateur (ex: 'fr' pour français)
    const browserLang = navigator.language.split('-')[0]
    
    const response = await fetch(
      `http://localhost:8000/api/cities/${encodeURIComponent(query)}?lang=${browserLang}`
    )
    if (!response.ok) throw new Error('Failed to fetch cities')
    cities.value = await response.json()
  } catch (error) {
    console.error('Error fetching cities:', error)
    cities.value = []
  }
}

// Création d'une version temporisée de fetchCities
// N'envoie la requête que 300ms après la dernière frappe
const debouncedFetchCities = debounce(fetchCities, 300)

// Gère la saisie de l'utilisateur dans le champ de recherche
const handleInput = () => {
  selectedCity.value = null  // Réinitialise la ville sélectionnée
  debouncedFetchCities(searchQuery.value)  // Lance la recherche
}

// Fonction appelée quand l'utilisateur sélectionne une ville
const selectCity = (city: City) => {
  selectedCity.value = city          // Stocke la ville sélectionnée
  searchQuery.value = city.name      // Met à jour le champ de recherche
  cities.value = []                  // Cache la liste des suggestions
}
</script>

<style scoped>
.city-search {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
}

.search-container {
  position: relative;
}

.search-input {
  width: 100%;
  padding: 1rem 1.5rem;
  font-size: 1.1rem;
  border: 2px solid var(--border-color);
  border-radius: 12px;
  background-color: var(--surface-color);
  color: var(--text-color);
  transition: all 0.3s ease;
  box-shadow: var(--shadow);
}

.search-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.2);
  outline: none;
}

.city-list {
  position: absolute;
  width: 100%;
  max-height: 350px;
  overflow-y: auto;
  margin-top: 0.5rem;
  padding: 0.5rem;
  list-style: none;
  background: var(--surface-color);
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.city-list::-webkit-scrollbar {
  width: 8px;
}

.city-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.city-list::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.city-item {
  padding: 0.8rem 1rem;
  margin: 0.25rem 0;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.city-item:hover {
  background-color: rgba(76, 175, 80, 0.1);
  transform: translateX(4px);
}

.city-item-name {
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 0.25rem;
}

.city-item-details {
  font-size: 0.9rem;
  color: #666;
}

.city-details {
  margin-top: 2rem;
  padding: 2rem;
  background-color: var(--surface-color);
  border-radius: 12px;
  box-shadow: var(--shadow);
  animation: fadeIn 0.3s ease-out;
}

.city-details h2 {
  color: var(--primary-color);
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  border-bottom: 2px solid var(--primary-color);
  padding-bottom: 0.5rem;
  display: inline-block;
}

.city-details p {
  margin: 0.75rem 0;
  font-size: 1.1rem;
  color: var(--text-color);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .search-input {
    font-size: 1rem;
    padding: 0.8rem 1.2rem;
  }

  .city-details {
    padding: 1.5rem;
  }
}
</style>
