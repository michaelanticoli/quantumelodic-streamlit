"""
Quantumelodic MetaSystem Core
A system for translating astrological data into unique musical compositions
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Tuple
import numpy as np

class QuantumelodicMetaSystem:
    """Core system for astrological-musical translation"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_base = "https://api.freeastrologyapi.com/api/v3/native"
        
        # Musical mappings from your dataset
        self.planetary_modes = {
            'Sun': {'mode': 'Ionian', 'tonic': 'E', 'tempo': 120, 'instruments': ['Brass', 'Trumpets']},
            'Moon': {'mode': 'Aeolian', 'tonic': 'F', 'tempo': 60, 'instruments': ['Piano', 'Cello']},
            'Mercury': {'mode': 'Mixolydian', 'tonic': 'D', 'tempo': 130, 'instruments': ['Flutes', 'Clarinets']},
            'Venus': {'mode': 'Lydian', 'tonic': 'G', 'tempo': 70, 'instruments': ['Strings', 'Harp']},
            'Mars': {'mode': 'Phrygian', 'tonic': 'C', 'tempo': 160, 'instruments': ['Percussion', 'Electric Guitar']},
            'Jupiter': {'mode': 'Lydian', 'tonic': 'A', 'tempo': 100, 'instruments': ['Brass', 'Timpani']},
            'Saturn': {'mode': 'Dorian', 'tonic': 'B', 'tempo': 60, 'instruments': ['Bassoon', 'Organ']},
            'Uranus': {'mode': 'Aeolian', 'tonic': 'Ab', 'tempo': 140, 'instruments': ['Synthesizers']},
            'Neptune': {'mode': 'Ionian', 'tonic': 'Bb', 'tempo': 50, 'instruments': ['Harp', 'Synths']},
            'Pluto': {'mode': 'Phrygian', 'tonic': 'Db', 'tempo': 90, 'instruments': ['Low Brass', 'Percussion']}
        }
        
        self.aspect_intervals = {
            'conjunction': {'interval': 'unison', 'harmony': 'consonant'},
            'sextile': {'interval': 'major_6th', 'harmony': 'consonant'},
            'trine': {'interval': 'perfect_5th', 'harmony': 'consonant'},
            'square': {'interval': 'minor_2nd', 'harmony': 'dissonant'},
            'opposition': {'interval': 'octave', 'harmony': 'tense'},
            'quincunx': {'interval': 'minor_7th', 'harmony': 'unresolved'}
        }
        
        self.sign_modifiers = {
            'Aries': {'tempo_mult': 1.2, 'intensity': 'forte'},
            'Taurus': {'tempo_mult': 0.8, 'intensity': 'mezzo-forte'},
            'Gemini': {'tempo_mult': 1.1, 'intensity': 'varied'},
            'Cancer': {'tempo_mult': 0.9, 'intensity': 'piano'},
            'Leo': {'tempo_mult': 1.0, 'intensity': 'forte'},
            'Virgo': {'tempo_mult': 0.95, 'intensity': 'mezzo-piano'},
            'Libra': {'tempo_mult': 0.9, 'intensity': 'balanced'},
            'Scorpio': {'tempo_mult': 0.85, 'intensity': 'deep'},
            'Sagittarius': {'tempo_mult': 1.15, 'intensity': 'expansive'},
            'Capricorn': {'tempo_mult': 0.75, 'intensity': 'structured'},
            'Aquarius': {'tempo_mult': 1.05, 'intensity': 'eccentric'},
            'Pisces': {'tempo_mult': 0.8, 'intensity': 'fluid'}
        }
    
    def fetch_natal_chart(self, birth_data: Dict) -> Dict:
        """Fetch natal chart data from API"""
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }
        
        # Prepare request data
        request_data = {
            "name": birth_data.get("name", "User"),
            "year": birth_data["year"],
            "month": birth_data["month"],
            "day": birth_data["day"],
            "hour": birth_data["hour"],
            "minute": birth_data["minute"],
            "latitude": birth_data["latitude"],
            "longitude": birth_data["longitude"],
            "timezone": birth_data.get("timezone", "America/New_York"),
            "settings": {
                "observation_point": "topocentric",
                "ayanamsha": "lahiri"
            }
        }
        
        try:
            response = requests.post(
                f"{self.api_base}/natal-chart",
                headers=headers,
                json=request_data
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching natal chart: {e}")
            return None
    
    def calculate_frequencies(self, chart_data: Dict) -> Dict:
        """Calculate unique frequencies based on planetary positions"""
        frequencies = {}
        base_frequency = 432.0  # A4 = 432 Hz (cosmic tuning)
        
        if not chart_data:
            return frequencies
            
        planets = chart_data.get('planets', {})
        
        for planet, data in planets.items():
            if planet in self.planetary_modes:
                # Get base note frequency
                note = self.planetary_modes[planet]['tonic']
                sign = data.get('sign', 'Aries')
                degree = data.get('degree', 0)
                
                # Calculate unique frequency based on position
                # This creates a unique frequency for each planetary position
                frequency_modifier = 1 + (degree / 360)  # 1.0 to 1.0833
                sign_modifier = hash(sign) % 12 / 12  # 0 to 1 based on sign
                
                # Create unique frequency
                planet_freq = base_frequency * frequency_modifier * (1 + sign_modifier * 0.1)
                
                frequencies[planet] = {
                    'frequency': round(planet_freq, 2),
                    'mode': self.planetary_modes[planet]['mode'],
                    'tempo': int(self.planetary_modes[planet]['tempo'] * 
                                self.sign_modifiers.get(sign, {}).get('tempo_mult', 1.0)),
                    'instruments': self.planetary_modes[planet]['instruments'],
                    'sign': sign,
                    'degree': degree
                }
        
        return frequencies
    
    def generate_aspect_harmonics(self, chart_data: Dict) -> List[Dict]:
        """Generate harmonic relationships based on aspects"""
        aspects = []
        aspect_data = chart_data.get('aspects', [])
        
        for aspect in aspect_data:
            if aspect['aspect_name'].lower() in self.aspect_intervals:
                interval_data = self.aspect_intervals[aspect['aspect_name'].lower()]
                aspects.append({
                    'planets': [aspect['planet1'], aspect['planet2']],
                    'type': aspect['aspect_name'],
                    'orb': aspect['orb'],
                    'interval': interval_data['interval'],
                    'harmony': interval_data['harmony'],
                    'strength': 1 - (abs(aspect['orb']) / 8)  # Strength based on orb
                })
        
        return aspects
    
    def create_musical_structure(self, frequencies: Dict, aspects: List[Dict]) -> Dict:
        """Create the overall musical structure"""
        structure = {
            'key_signature': self._determine_key_signature(frequencies),
            'time_signature': self._determine_time_signature(frequencies),
            'tempo': self._calculate_overall_tempo(frequencies),
            'sections': self._create_sections(frequencies, aspects),
            'progression': self._create_chord_progression(frequencies, aspects)
        }
        
        return structure
    
    def _determine_key_signature(self, frequencies: Dict) -> str:
        """Determine overall key based on Sun, Moon, and Ascendant"""
        # Priority: Sun > Ascendant > Moon
        if 'Sun' in frequencies:
            return frequencies['Sun']['mode']
        elif 'Ascendant' in frequencies:
            return frequencies['Ascendant']['mode']
        elif 'Moon' in frequencies:
            return frequencies['Moon']['mode']
        return 'Ionian'  # Default to major
    
    def _determine_time_signature(self, frequencies: Dict) -> str:
        """Determine time signature based on element distribution"""
        # This is a simplified version - could be enhanced
        cardinal_count = sum(1 for p in frequencies.values() 
                           if p['sign'] in ['Aries', 'Cancer', 'Libra', 'Capricorn'])
        
        if cardinal_count >= 3:
            return "4/4"  # Strong, driving rhythm
        elif any(p['sign'] in ['Gemini', 'Virgo', 'Sagittarius', 'Pisces'] 
                for p in frequencies.values()):
            return "6/8"  # Flowing, mutable
        else:
            return "3/4"  # Waltz-like, fixed
    
    def _calculate_overall_tempo(self, frequencies: Dict) -> int:
        """Calculate weighted average tempo"""
        if not frequencies:
            return 120
            
        total_tempo = 0
        weights = {'Sun': 3, 'Moon': 2, 'Ascendant': 2}
        total_weight = 0
        
        for planet, data in frequencies.items():
            weight = weights.get(planet, 1)
            total_tempo += data['tempo'] * weight
            total_weight += weight
        
        return int(total_tempo / total_weight) if total_weight > 0 else 120
    
    def _create_sections(self, frequencies: Dict, aspects: List[Dict]) -> List[Dict]:
        """Create musical sections based on house placements"""
        # Simplified version - would integrate house data
        sections = [
            {'name': 'Introduction', 'planets': ['Ascendant', 'Sun'], 'duration': 16},
            {'name': 'Development', 'planets': ['Mercury', 'Venus', 'Mars'], 'duration': 32},
            {'name': 'Climax', 'planets': ['Jupiter', 'Saturn'], 'duration': 16},
            {'name': 'Resolution', 'planets': ['Uranus', 'Neptune', 'Pluto'], 'duration': 24}
        ]
        return sections
    
    def _create_chord_progression(self, frequencies: Dict, aspects: List[Dict]) -> List[str]:
        """Create chord progression based on aspects"""
        progression = []
        
        # Start with tonic
        progression.append("I")
        
        # Add chords based on harmonious aspects
        for aspect in aspects:
            if aspect['harmony'] == 'consonant' and aspect['strength'] > 0.5:
                if aspect['interval'] == 'perfect_5th':
                    progression.append("V")
                elif aspect['interval'] == 'major_6th':
                    progression.append("vi")
            elif aspect['harmony'] == 'dissonant':
                progression.append("bII")  # Neapolitan
        
        # Return to tonic
        progression.append("I")
        
        return progression
    
    def generate_composition(self, birth_data: Dict) -> Dict:
        """Generate complete musical composition from birth data"""
        print("🌟 Fetching natal chart data...")
        chart_data = self.fetch_natal_chart(birth_data)
        
        if not chart_data:
            return None
        
        print("🎵 Calculating unique frequencies...")
        frequencies = self.calculate_frequencies(chart_data)
        
        print("🎼 Analyzing aspect harmonics...")
        aspects = self.generate_aspect_harmonics(chart_data)
        
        print("🎹 Creating musical structure...")
        structure = self.create_musical_structure(frequencies, aspects)
        
        composition = {
            'birth_data': birth_data,
            'frequencies': frequencies,
            'aspects': aspects,
            'structure': structure,
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'system_version': '1.0.0'
            }
        }
        
        return composition


# Example usage
if __name__ == "__main__":
    # Initialize system
    api_key = "Wno8gGxCZO91mq9qaRgqU8oJrMDZ6WXy4FQjua4t"
    qms = QuantumelodicMetaSystem(api_key)
    
    # Example birth data
    birth_data = {
        "name": "Example User",
        "year": 1985,
        "month": 4,
        "day": 24,
        "hour": 19,
        "minute": 55,
        "latitude": 40.7128,
        "longitude": -74.0060,
        "timezone": "America/New_York"
    }
    
    # Generate composition
    composition = qms.generate_composition(birth_data)
    
    if composition:
        print("\n✨ Composition Generated!")
        print(json.dumps(composition, indent=2))