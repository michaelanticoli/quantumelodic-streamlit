from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import csv
import os
import pandas as pd

app = FastAPI(title="Quantumelodies API", version="1.2")

# Load glossary from CSV file with normalized fields and support for category/aliases
def load_glossary_csv(path: str):
    glossary = []
    if not os.path.exists(path):
        return glossary
    with open(path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            aliases = [alias.strip().lower() for alias in row.get("aliases", "").split(",") if alias.strip()] if "aliases" in row else []
            glossary.append({
                "term": row.get("term", "").strip().lower(),
                "astrological_definition": row.get("definition", "").strip(),
                "musical_equivalent": row.get("musical_equivalent", "").strip(),
                "mathematical_equivalent": row.get("math_equivalent", "").strip(),
                "category": row.get("category", "").strip().lower() if "category" in row else "",
                "aliases": aliases
            })
    return glossary

# Load from a CSV file stored locally
GLOSSARY_CSV_PATH = "glossary.csv"
glossary_data = load_glossary_csv(GLOSSARY_CSV_PATH)

# Load planetary thematic mappings for musical interpretation
thematic_df = pd.read_csv("cleaned_Quantumelodic Dataset Official - Zodiacal-House-Planet Thematics.csv")

def find_theme(planet, sign, house):
    row = thematic_df[(thematic_df['Planet'].str.lower() == planet.lower()) &
                      (thematic_df['Sign'].str.lower() == sign.lower()) &
                      (thematic_df['House'].str.lower() == house.lower())]
    if not row.empty:
        r = row.iloc[0]
        return {
            "theme": r.get("Theme", ""),
            "mode": r.get("Mode", ""),
            "tempo": r.get("Tempo", ""),
            "instrumentation": r.get("Instrumentation", "")
        }
    else:
        return {
            "theme": f"{planet} in {sign}, {house} suggests a unique harmonic signature.",
            "mode": "Ionian",
            "tempo": "Moderate",
            "instrumentation": "Strings"
        }

class PlanetPlacement(BaseModel):
    planet: str
    sign: str
    house: str

class Aspect(BaseModel):
    between: List[str]
    type: str

class ChartData(BaseModel):
    placements: List[PlanetPlacement]
    aspects: Optional[List[Aspect]] = []

@app.get("/glossary/lookup")
def glossary_lookup(term: str = Query(..., description="Term to search for")):
    clean_term = term.strip().lower()
    result = next((item for item in glossary_data
                   if item["term"] == clean_term or clean_term in item.get("aliases", [])), None)
    return result or {"message": "Term not found."}

@app.get("/glossary/by-category")
def glossary_by_category(type: str = Query(..., description="Category to filter by")):
    filtered = [item for item in glossary_data if item.get("category") == type.strip().lower()]
    return filtered or {"message": "No terms found in this category."}

@app.post("/translate/chart-to-music")
def translate_chart(data: ChartData):
    result = []
    for placement in data.placements:
        musical_data = find_theme(placement.planet, placement.sign, placement.house)
        result.append({
            "planet": placement.planet,
            "theme": musical_data["theme"],
            "mode": musical_data["mode"],
            "tempo": musical_data["tempo"],
            "instrumentation": musical_data["instrumentation"]
        })
    return {"musical_interpretation": result}

@app.post("/generate/sound-map")
def generate_sound_map(aspect: Aspect):
    return {
        "aspect": f"{aspect.between[0]} {aspect.type} {aspect.between[1]}",
        "musical_effect": "Dissonant interplay resolving into harmonic resolution"
    }

if __name__ == "__main__":
    uvicorn.run("quantumelodies_api:app", host="0.0.0.0", port=8000, reload=True)
