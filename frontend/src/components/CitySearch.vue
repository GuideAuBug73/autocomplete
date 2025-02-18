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
/* Container principal du composant */
.city-search {
  max-width: 600px;         /* Limite la largeur pour une meilleure lisibilité */
  margin: 0 auto;          /* Centre le composant horizontalement */
  padding: 20px;           /* Espacement interne */
}

/* Conteneur du champ de recherche et de la liste des suggestions */
.search-container {
  position: relative;      /* Permet le positionnement absolu de la liste */
}

/* Style du champ de recherche */
.search-input {
  width: 100%;            /* Occupe toute la largeur disponible */
  padding: 12px;          /* Espacement interne confortable */
  font-size: 16px;        /* Taille de police lisible */
  border: 2px solid #ddd; /* Bordure visible mais subtile */
  border-radius: 8px;     /* Coins arrondis */
  outline: none;          /* Supprime le contour par défaut */
  transition: border-color 0.3s;  /* Animation de la bordure */
}

/* Style du champ de recherche quand il a le focus */
.search-input:focus {
  border-color: #4CAF50;  /* Bordure verte pour indiquer le focus */
}

/* Liste déroulante des suggestions */
.city-list {
  position: absolute;      /* Positionnement par rapport au conteneur */
  width: 100%;            /* Même largeur que le champ de recherche */
  max-height: 300px;      /* Hauteur maximum avant défilement */
  overflow-y: auto;       /* Barre de défilement si nécessaire */
  list-style: none;       /* Supprime les puces de liste */
  padding: 0;
  margin: 0;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: #f8f9fa;    /* Fond plus contrasté */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);  /* Ombre légère */
  z-index: 1000;          /* S'affiche au-dessus des autres éléments */
}

/* Style des éléments de la liste */
.city-item {
  padding: 12px;          /* Espacement interne */
  cursor: pointer;        /* Indique que l'élément est cliquable */
  transition: background-color 0.2s;  /* Animation au survol */
  border-bottom: 1px solid #e9ecef;  /* Séparateur entre les éléments */
}

.city-item:last-child {
  border-bottom: none;    /* Pas de bordure pour le dernier élément */
}

/* Style au survol des éléments de la liste */
.city-item:hover {
  background-color: #e9ecef;  /* Fond plus contrasté au survol */
}

/* Nom de la ville dans la liste */
.city-item-name {
  font-weight: 500;       /* Police un peu plus grasse */
  color: #212529;         /* Couleur plus foncée pour meilleur contraste */
  margin-bottom: 4px;     /* Espacement avec les détails */
}

/* Détails de la ville dans la liste */
.city-item-details {
  font-size: 0.9em;      /* Taille de police légèrement plus petite */
  color: #6c757d;        /* Couleur grise mais lisible */
}

/* Section affichant les détails de la ville */
.city-details {
  margin-top: 30px;       /* Espacement avec le champ de recherche */
  padding: 20px;
  border-radius: 8px;
  background-color: #f8f9fa;  /* Fond plus contrasté */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);  /* Ombre très légère */
}

/* Titre dans les détails de la ville */
.city-details h2 {
  margin: 0 0 15px 0;
  color: #212529;         /* Couleur plus foncée pour meilleur contraste */
  font-weight: 600;      /* Police plus grasse */
}

/* Paragraphes dans les détails de la ville */
.city-details p {
  margin: 8px 0;
  color: #495057;         /* Couleur plus foncée pour meilleur contraste */
}
</style>
