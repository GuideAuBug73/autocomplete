# Ce fichier est le point d'entrée du backend de l'application
# Il fournit une API pour rechercher des villes en utilisant le service Geoapify

# Importation des modules nécessaires
from fastapi import FastAPI, HTTPException  # Framework web pour créer l'API
from fastapi.middleware.cors import CORSMiddleware  # Pour gérer les requêtes cross-origin
import httpx  # Client HTTP asynchrone pour faire des requêtes à l'API Geoapify
from typing import List  # Pour le typage des données
import os  # Pour accéder aux variables d'environnement
from dotenv import load_dotenv  # Pour charger les variables d'environnement depuis .env

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()

# Création de l'application FastAPI
app = FastAPI()

# Configuration CORS (Cross-Origin Resource Sharing)
# Cela permet au frontend d'envoyer des requêtes au backend même s'ils sont sur des domaines différents
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines (à configurer en production)
    allow_credentials=True,  # Autorise l'envoi de cookies
    allow_methods=["*"],  # Autorise toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Autorise tous les headers HTTP
)

# Récupération de la clé API Geoapify depuis les variables d'environnement
GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")
# Vérifie que la clé API est bien définie
if not GEOAPIFY_API_KEY:
    raise ValueError("GEOAPIFY_API_KEY environment variable is not set")

# Définition de l'endpoint /api/cities/{query}
# Ce endpoint permet de rechercher des villes en fonction d'une chaîne de recherche
@app.get("/api/cities/{query}")
async def search_cities(query: str, lang: str = "en") -> List[dict]:
    # Ne recherche que si la requête contient au moins 3 caractères
    if len(query) < 3:
        return []
    
    # Création d'un client HTTP asynchrone pour faire la requête à Geoapify
    async with httpx.AsyncClient() as client:
        # Appel à l'API Geoapify avec les paramètres suivants:
        response = await client.get(
            "https://api.geoapify.com/v1/geocode/autocomplete",
            params={
                "text": query,      # Le texte de recherche
                "type": "city",     # Ne chercher que des villes
                "format": "json",   # Format de réponse souhaité
                "apiKey": GEOAPIFY_API_KEY,  # Clé API requise
                "limit": 5,        # Limite le nombre de résultats à 5
                "lang": lang       # Langue des résultats (ex: fr, en, de, etc.)
            }
        )
        
        # Vérifie si la requête a réussi (code 200)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from Geoapify")
        
        # Convertit la réponse JSON en dictionnaire Python
        data = response.json()
        results = []
        
        # Traitement des résultats de l'API
        for result in data.get("results", []):
            # Récupère le nom de la ville (utilise 'formatted' si 'city' n'existe pas)
            city_name = result.get("city") or result.get("formatted")
            if city_name:
                # Crée un dictionnaire avec les informations détaillées de la ville
                results.append({
                    "name": city_name,                    # Nom de la ville
                    "country": result.get("country"),     # Pays
                    "state": result.get("state"),         # État/Région
                    "county": result.get("county"),       # Département/Comté
                    "lat": result.get("lat"),            # Latitude
                    "lon": result.get("lon")             # Longitude
                })
        
        # Retourne la liste des villes trouvées
        return results
