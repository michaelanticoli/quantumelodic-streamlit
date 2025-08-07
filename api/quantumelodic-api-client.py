"""
Quantumelodic API Client for Free Astrology API Integration
Handles all communication with the astrology API and data transformation
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import pytz

@dataclass
class BirthData:
    """Data class for birth information"""
    name: str
    year: int
    month: int
    day: int
    hour: int
    minute: int
    latitude: float
    longitude: float
    timezone: str = "UTC"

class AstrologyAPIClient:
    """Client for Free Astrology API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.freeastrologyapi.com/api/v3"
        self.headers = {
            'Content-Type': 'application/json',
            'x-api-key': api_key
        }
    
    def get_natal_chart(self, birth_data: BirthData) -> Dict:
        """Fetch complete natal chart with planets, houses, and aspects"""
        
        # Prepare request payload
        payload = {
            "name": birth_data.name,
            "year": birth_data.year,
            "month": birth_data.month,
            "day": birth_data.day,
            "hour": birth_data.hour,
            "minute": birth_data.minute,
            "latitude": birth_data.latitude,
            "longitude": birth_data.longitude,
            "timezone": birth_data.timezone,
            "settings": {
                "observation_point": "topocentric",
                "ayanamsha": "lahiri",
                "language": "en"
            }
        }
        
        try:
            # Get natal wheel (planets and houses)
            response = requests.post(
                f"{self.base_url}/native/natal-wheel-chart",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            natal_data = response.json()
            
            # Get aspects
            aspects_response = requests.post(
                f"{self.base_url}/native/aspects",
                headers=self.headers,
                json=payload
            )
            aspects_response.raise_for_status()
            aspects_data = aspects_response.json()
            
            # Combine data
            return {
                'natal_wheel': natal_data,
                'aspects': aspects_data,
                'birth_data': birth_data.__dict__
            }
            
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return None
    
    def get_current_transits(self, birth_data: BirthData) -> Dict:
        """Get current planetary transits"""
        
        # Current date/time
        now = datetime.now(pytz.timezone(birth_data.timezone))
        
        transit_payload = {
            "name": birth_data.name,
            "year": birth_data.year,
            "month": birth_data.month,
            "day": birth_data.day,
            "hour": birth_data.hour,
            "minute": birth_data.minute,
            "latitude": birth_data.latitude,
            "longitude": birth_data.longitude,
            "timezone": birth_data.timezone,
            "current_year": now.year,
            "current_month": now.month,
            "current_day": now.day,
            "current_hour": now.hour,
            "current_minute": now.minute,
            "settings": {
                "observation_point": "topocentric",
                "ayanamsha": "lahiri"
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/native/transits",
                headers=self.headers,
                json=transit_payload
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Transit API Error: {e}")
            return None


class QuantumelodicDataTransformer:
    """Transform astrological data into musical parameters"""
    
    def __init__(self):
        # Sign to element mapping
        self.sign_elements = {
            'Aries': 'Fire', 'Leo': 'Fire', 'Sagittarius': 'Fire',
            'Taurus': 'Earth', 'Virgo': 'Earth', 'Capricorn': 'Earth',
            'Gemini': 'Air', 'Libra': 'Air', 'Aquarius': 'Air',
            'Cancer': 'Water', 'Scorpio': 'Water', 'Pisces': 'Water'
        }
        
        # Musical mode assignments
        self.planetary_modes = {
            'Sun': 'Ionian',
            'Moon': 'Aeolian',
            'Mercury': 'Mixolydian',
            'Venus': 'Lydian',
            'Mars': 'Phrygian',
            'Jupiter': 'Lydian',
            'Saturn': 'Dorian',
            'Uranus': 'Aeolian',
            'Neptune': 'Ionian',
            'Pluto': 'Phrygian',
            'North Node': 'Locrian',
            'Chiron': 'Dorian'
        }
    
    def transform_natal_chart(self, api_data: Dict) -> Dict:
        """Transform API data into Quantumelodic format"""
        
        if not api_data or 'natal_wheel' not in api_data:
            return None
        
        natal_wheel = api_data['natal_wheel']
        aspects = api_data.get('aspects', {})
        
        # Extract planetary data
        planets = {}
        if 'planets' in natal_wheel:
            for planet_data in natal_wheel['planets']:
                planet_name = planet_data['name']
                planets[planet_name] = {
                    'sign': planet_data['sign'],
                    'degree': planet_data['degree'],
                    'house': planet_data.get('house', 1),
                    'retrograde': planet_data.get('retrograde', False),
                    'element': self.sign_elements.get(planet_data['sign'], 'Earth'),
                    'mode': self.planetary_modes.get(planet_name, 'Ionian')
                }
        
        # Extract house data
        houses = {}
        if 'houses' in natal_wheel:
            for i, house in enumerate(natal_wheel['houses'], 1):
                houses[f'House_{i}'] = {
                    'sign': house['sign'],
                    'degree': house['degree']
                }
        
        # Transform aspects
        transformed_aspects = []
        if 'aspects' in aspects:
            for aspect in aspects['aspects']:
                transformed_aspects.append({
                    'planet1': aspect['planet1'],
                    'planet2': aspect['planet2'],
                    'aspect_type': aspect['aspect_name'],
                    'orb': aspect['orb'],
                    'exact_degree': aspect.get('exact_degree', 0),
                    'applying': aspect.get('applying', False)
                })
        
        # Calculate element distribution
        element_distribution = self._calculate_element_distribution(planets)
        
        # Calculate modality distribution
        modality_distribution = self._calculate_modality_distribution(planets)
        
        return {
            'planets': planets,
            'houses': houses,
            'aspects': transformed_aspects,
            'element_distribution': element_distribution,
            'modality_distribution': modality_distribution,
            'chart_pattern': self._identify_chart_pattern(planets, transformed_aspects),
            'dominant_element': max(element_distribution, key=element_distribution.get),
            'birth_data': api_data.get('birth_data', {})
        }
    
    def _calculate_element_distribution(self, planets: Dict) -> Dict:
        """Calculate distribution of elements in chart"""
        distribution = {'Fire': 0, 'Earth': 0, 'Air': 0, 'Water': 0}
        
        # Weight different planets
        weights = {
            'Sun': 3, 'Moon': 3, 'Ascendant': 3,
            'Mercury': 2, 'Venus': 2, 'Mars': 2,
            'Jupiter': 1.5, 'Saturn': 1.5,
            'Uranus': 1, 'Neptune': 1, 'Pluto': 1
        }
        
        for planet, data in planets.items():
            weight = weights.get(planet, 1)
            element = data.get('element', 'Earth')
            distribution[element] += weight
        
        # Normalize
        total = sum(distribution.values())
        if total > 0:
            distribution = {k: v/total for k, v in distribution.items()}
        
        return distribution
    
    def _calculate_modality_distribution(self, planets: Dict) -> Dict:
        """Calculate distribution of modalities in chart"""
        modalities = {
            'Cardinal': ['Aries', 'Cancer', 'Libra', 'Capricorn'],
            'Fixed': ['Taurus', 'Leo', 'Scorpio', 'Aquarius'],
            'Mutable': ['Gemini', 'Virgo', 'Sagittarius', 'Pisces']
        }
        
        distribution = {'Cardinal': 0, 'Fixed': 0, 'Mutable': 0}
        
        for planet, data in planets.items():
            sign = data.get('sign', '')
            for modality, signs in modalities.items():
                if sign in signs:
                    distribution[modality] += 1
                    break
        
        return distribution
    
    def _identify_chart_pattern(self, planets: Dict, aspects: List) -> str:
        """Identify major chart patterns"""
        # Simplified pattern recognition
        aspect_count = len(aspects)
        
        # Count different aspect types
        aspect_types = {}
        for aspect in aspects:
            aspect_type = aspect['aspect_type']
            aspect_types[aspect_type] = aspect_types.get(aspect_type, 0) + 1
        
        # Basic pattern identification
        if aspect_types.get('trine', 0) >= 3:
            return 'Grand Trine'
        elif aspect_types.get('square', 0) >= 4:
            return 'Grand Cross'
        elif aspect_types.get('opposition', 0) >= 2 and aspect_types.get('sextile', 0) >= 2:
            return 'Mystic Rectangle'
        elif aspect_count > 15:
            return 'Highly Aspected'
        elif aspect_count < 5:
            return 'Lightly Aspected'
        else:
            return 'Mixed Aspects'


# Integration with main Quantumelodic system
class QuantumelodicAPIIntegration:
    """Complete integration of API with Quantumelodic system"""
    
    def __init__(self, api_key: str):
        self.api_client = AstrologyAPIClient(api_key)
        self.transformer = QuantumelodicDataTransformer()
    
    def process_birth_chart(self, birth_data: BirthData) -> Dict:
        """Complete processing pipeline"""
        
        print("🌟 Fetching astrological data...")
        raw_data = self.api_client.get_natal_chart(birth_data)
        
        if not raw_data:
            print("❌ Failed to fetch astrological data")
            return None
        
        print("🔄 Transforming data for musical synthesis...")
        transformed_data = self.transformer.transform_natal_chart(raw_data)
        
        print("🎵 Adding current transits...")
        transits = self.api_client.get_current_transits(birth_data)
        if transits:
            transformed_data['current_transits'] = transits
        
        return transformed_data
    
    def get_birth_data_from_input(self, user_input: Dict) -> BirthData:
        """Convert user input to BirthData object"""
        return BirthData(
            name=user_input.get('name', 'User'),
            year=user_input['year'],
            month=user_input['month'],
            day=user_input['day'],
            hour=user_input['hour'],
            minute=user_input['minute'],
            latitude=user_input['latitude'],
            longitude=user_input['longitude'],
            timezone=user_input.get('timezone', 'UTC')
        )


# Example usage
if __name__ == "__main__":
    api_key = "Wno8gGxCZO91mq9qaRgqU8oJrMDZ6WXy4FQjua4t"
    integration = QuantumelodicAPIIntegration(api_key)
    
    # Example birth data
    birth_data = BirthData(
        name="Example User",
        year=1985,
        month=4,
        day=24,
        hour=19,
        minute=55,
        latitude=40.7128,
        longitude=-74.0060,
        timezone="America/New_York"
    )
    
    # Process chart
    result = integration.process_birth_chart(birth_data)
    
    if result:
        print("\n✨ Chart processed successfully!")
        print(f"Dominant Element: {result['dominant_element']}")
        print(f"Chart Pattern: {result['chart_pattern']}")
        print(f"Number of Aspects: {len(result['aspects'])}")
