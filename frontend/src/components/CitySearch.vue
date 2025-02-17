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
          {{ city.name }}
        </li>
      </ul>
    </div>

    <div v-if="selectedCity" class="city-details">
      <h2>{{ selectedCity.name }}</h2>
      <p>Latitude: {{ selectedCity.lat }}</p>
      <p>Longitude: {{ selectedCity.lon }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { debounce } from 'lodash'

interface City {
  name: string
  lat: number
  lon: number
}

const searchQuery = ref('')
const cities = ref<City[]>([])
const selectedCity = ref<City | null>(null)

const fetchCities = async (query: string) => {
  if (query.length < 2) {
    cities.value = []
    return
  }

  try {
    const response = await fetch(`http://localhost:8000/api/cities/${encodeURIComponent(query)}`)
    if (!response.ok) throw new Error('Failed to fetch cities')
    cities.value = await response.json()
  } catch (error) {
    console.error('Error fetching cities:', error)
    cities.value = []
  }
}

const debouncedFetchCities = debounce(fetchCities, 300)

const handleInput = () => {
  selectedCity.value = null
  debouncedFetchCities(searchQuery.value)
}

const selectCity = (city: City) => {
  selectedCity.value = city
  searchQuery.value = city.name
  cities.value = []
}
</script>

<style scoped>
.city-search {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.search-container {
  position: relative;
}

.search-input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 2px solid #ddd;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.3s;
}

.search-input:focus {
  border-color: #4CAF50;
}

.city-list {
  position: absolute;
  width: 100%;
  max-height: 300px;
  overflow-y: auto;
  list-style: none;
  padding: 0;
  margin: 0;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.city-item {
  padding: 12px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.city-item:hover {
  background-color: #f5f5f5;
}

.city-details {
  margin-top: 30px;
  padding: 20px;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.city-details h2 {
  margin: 0 0 15px 0;
  color: #333;
}

.city-details p {
  margin: 8px 0;
  color: #666;
}
</style>
