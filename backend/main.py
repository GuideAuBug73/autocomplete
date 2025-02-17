from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")
if not GEOAPIFY_API_KEY:
    raise ValueError("GEOAPIFY_API_KEY environment variable is not set")

@app.get("/api/cities/{query}")
async def search_cities(query: str) -> List[dict]:
    if len(query) < 3:
        return []
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.geoapify.com/v1/geocode/autocomplete",
            params={
                "text": query,
                "type": "city",
                "format": "json",
                "apiKey": GEOAPIFY_API_KEY,
                "limit": 5
            }
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from Geoapify")
        
        data = response.json()
        results = []
        
        for result in data.get("results", []):
            city_name = result.get("city") or result.get("formatted")
            if city_name:
                results.append({
                    "name": city_name,
                    "lat": result.get("lat"),
                    "lon": result.get("lon")
                })
        
        return results
