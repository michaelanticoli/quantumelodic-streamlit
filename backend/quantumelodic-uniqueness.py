"""
Advanced Uniqueness Algorithm for Quantumelodic MetaSystem
Ensures each natal chart produces a truly unique musical composition
"""

import numpy as np
from typing import Dict, List, Tuple
import hashlib
from datetime import datetime

class QuantumelodicUniqueness:
    """Advanced algorithms for ensuring musical uniqueness"""
    
    def __init__(self):
        # Sacred geometry ratios
        self.phi = 1.618033988749895  # Golden ratio
        self.sacred_ratios = {
            'unison': 1/1,
            'minor_second': 16/15,
            'major_second': 9/8,
            'minor_third': 6/5,
            'major_third': 5/4,
            'perfect_fourth': 4/3,
            'tritone': 45/32,
            'perfect_fifth': 3/2,
            'minor_sixth': 8/5,
            'major_sixth': 5/3,
            'minor_seventh': 16/9,
            'major_seventh': 15/8,
            'octave': 2/1
        }
        
        # Planetary orbital periods (in Earth days) for rhythm generation
        self.orbital_periods = {
            'Mercury': 87.97,
            'Venus': 224.70,
            'Mars': 686.98,
            'Jupiter': 4332.59,
            'Saturn': 10759.22,
            'Uranus': 30688.5,
            'Neptune': 60195.0,
            'Pluto': 90560.0
        }
        
        # Element frequencies (Hz) based on atomic vibrations
        self.element_frequencies = {
            'Fire': 528.0,    # Transformation frequency
            'Earth': 396.0,   # Grounding frequency
            'Air': 741.0,     # Expression frequency
            'Water': 639.0    # Flow frequency
        }
    
    def calculate_unique_frequency(self, planet: str, sign: str, degree: float, 
                                 minute: float, house: int) -> Dict:
        """
        Calculate a truly unique frequency based on multiple factors
        """
        # Base frequency from planet-sign combination
        base_freq = self._get_base_frequency(planet, sign)
        
        # Degree modifier (using golden ratio)
        degree_total = degree + (minute / 60)
        degree_modifier = 1 + (degree_total / 360) * (self.phi - 1)
        
        # House modifier (using harmonic series)
        house_harmonic = 1 + (house - 1) / 12
        
        # Time-based uniqueness (birth moment precision)
        time_hash = self._generate_time_hash(planet, degree_total)
        time_modifier = 1 + (time_hash % 1000) / 10000  # 0.1% to 10.1% variation
        
        # Calculate final frequency
        final_frequency = base_freq * degree_modifier * house_harmonic * time_modifier
        
        # Calculate harmonics (overtones)
        harmonics = self._calculate_harmonics(final_frequency, planet)
        
        # Calculate rhythm pattern based on orbital period
        rhythm_pattern = self._generate_rhythm_pattern(planet, sign)
        
        return {
            'fundamental': round(final_frequency, 3),
            'harmonics': harmonics,
            'rhythm_pattern': rhythm_pattern,
            'timbre_modifier': self._calculate_timbre(planet, sign, house),
            'amplitude_envelope': self._generate_envelope(planet, sign)
        }
    
    def _get_base_frequency(self, planet: str, sign: str) -> float:
        """Get base frequency using planet-sign matrix"""
        # Using a more complex calculation based on your interval matrix
        planet_base = {
            'Sun': 261.63,    # C4
            'Moon': 293.66,   # D4
            'Mercury': 329.63, # E4
            'Venus': 349.23,  # F4
            'Mars': 392.00,   # G4
            'Jupiter': 440.00, # A4
            'Saturn': 493.88, # B4
            'Uranus': 523.25, # C5
            'Neptune': 587.33, # D5
            'Pluto': 659.25   # E5
        }
        
        sign_modifier = {
            'Aries': self.sacred_ratios['major_third'],
            'Taurus': self.sacred_ratios['perfect_fourth'],
            'Gemini': self.sacred_ratios['major_second'],
            'Cancer': self.sacred_ratios['minor_sixth'],
            'Leo': self.sacred_ratios['perfect_fifth'],
            'Virgo': self.sacred_ratios['minor_third'],
            'Libra': self.sacred_ratios['major_sixth'],
            'Scorpio': self.sacred_ratios['tritone'],
            'Sagittarius': self.sacred_ratios['major_seventh'],
            'Capricorn': self.sacred_ratios['minor_seventh'],
            'Aquarius': self.sacred_ratios['major_second'] * 2,
            'Pisces': self.sacred_ratios['octave']
        }
        
        return planet_base.get(planet, 440.0) * sign_modifier.get(sign, 1.0)
    
    def _generate_time_hash(self, planet: str, degree: float) -> int:
        """Generate unique hash based on precise birth moment"""
        # Create a unique string from planet position
        unique_string = f"{planet}_{degree}_{datetime.now().timestamp()}"
        hash_object = hashlib.sha256(unique_string.encode())
        return int(hash_object.hexdigest(), 16)
    
    def _calculate_harmonics(self, fundamental: float, planet: str) -> List[float]:
        """Calculate overtones based on planetary characteristics"""
        harmonic_profiles = {
            'Sun': [1, 2, 3, 4, 5],      # Full harmonic series
            'Moon': [1, 2, 4, 8],         # Octaves only
            'Mercury': [1, 3, 5, 7, 9],   # Odd harmonics
            'Venus': [1, 2, 3, 5, 8],     # Fibonacci harmonics
            'Mars': [1, 2, 4, 5, 7],      # Power harmonics
            'Jupiter': [1, 2, 3, 4, 6],   # Expansion harmonics
            'Saturn': [1, 2, 4],          # Structural harmonics
            'Uranus': [1, 3, 7, 11],      # Prime harmonics
            'Neptune': [1, 2, 3, 6, 9],   # Mystical harmonics
            'Pluto': [1, 2, 5, 8, 13]     # Transformative harmonics
        }
        
        profile = harmonic_profiles.get(planet, [1, 2, 3])
        return [round(fundamental * h, 3) for h in profile]
    
    def _generate_rhythm_pattern(self, planet: str, sign: str) -> Dict:
        """Generate unique rhythm based on orbital mechanics"""
        # Base rhythm from orbital period
        orbital_rhythm = self.orbital_periods.get(planet, 365.25)
        
        # Normalize to musical tempo (60-180 BPM)
        base_tempo = 60 + (orbital_rhythm % 120)
        
        # Sign modifies the rhythm pattern
        sign_patterns = {
            'Cardinal': {'pattern': [1, 0, 0, 1], 'subdivision': 4},
            'Fixed': {'pattern': [1, 1, 1, 1], 'subdivision': 4},
            'Mutable': {'pattern': [1, 0, 1, 0, 1, 0], 'subdivision': 6}
        }
        
        sign_quality = self._get_sign_quality(sign)
        pattern_info = sign_patterns.get(sign_quality, sign_patterns['Cardinal'])
        
        return {
            'tempo': round(base_tempo, 1),
            'pattern': pattern_info['pattern'],
            'subdivision': pattern_info['subdivision'],
            'swing_factor': 0.5 + (hash(sign) % 50) / 100  # 0.5 to 1.0
        }
    
    def _calculate_timbre(self, planet: str, sign: str, house: int) -> Dict:
        """Calculate unique timbre characteristics"""
        # Waveform selection based on planet
        waveforms = {
            'Sun': 'sawtooth',     # Bright, full spectrum
            'Moon': 'sine',        # Pure, emotional
            'Mercury': 'square',   # Clear, articulate
            'Venus': 'triangle',   # Smooth, warm
            'Mars': 'sawtooth',    # Aggressive, cutting
            'Jupiter': 'complex',  # Rich harmonics
            'Saturn': 'square',    # Structured
            'Uranus': 'noise',     # Experimental
            'Neptune': 'sine_pad', # Ethereal
            'Pluto': 'pulse'       # Intense
        }
        
        # Filter characteristics based on sign element
        element = self._get_sign_element(sign)
        filter_config = {
            'Fire': {'type': 'highpass', 'cutoff': 800, 'resonance': 0.7},
            'Earth': {'type': 'lowpass', 'cutoff': 400, 'resonance': 0.3},
            'Air': {'type': 'bandpass', 'cutoff': 1200, 'resonance': 0.5},
            'Water': {'type': 'lowpass', 'cutoff': 600, 'resonance': 0.6}
        }
        
        return {
            'waveform': waveforms.get(planet, 'sine'),
            'filter': filter_config.get(element, filter_config['Earth']),
            'modulation_depth': house / 12,  # 0.083 to 1.0
            'detune_cents': (house - 6.5) * 2  # -11 to +11 cents
        }
    
    def _generate_envelope(self, planet: str, sign: str) -> Dict:
        """Generate ADSR envelope based on astrological factors"""
        # Planet determines basic envelope shape
        planet_envelopes = {
            'Sun': {'attack': 0.1, 'decay': 0.2, 'sustain': 0.8, 'release': 0.5},
            'Moon': {'attack': 0.3, 'decay': 0.4, 'sustain': 0.5, 'release': 1.0},
            'Mercury': {'attack': 0.01, 'decay': 0.1, 'sustain': 0.4, 'release': 0.2},
            'Venus': {'attack': 0.5, 'decay': 0.3, 'sustain': 0.7, 'release': 0.8},
            'Mars': {'attack': 0.001, 'decay': 0.05, 'sustain': 0.9, 'release': 0.1},
            'Jupiter': {'attack': 0.2, 'decay': 0.3, 'sustain': 0.9, 'release': 0.6},
            'Saturn': {'attack': 0.8, 'decay': 0.5, 'sustain': 0.6, 'release': 1.5},
            'Uranus': {'attack': 0.001, 'decay': 0.001, 'sustain': 0.3, 'release': 0.01},
            'Neptune': {'attack': 2.0, 'decay': 1.0, 'sustain': 0.7, 'release': 3.0},
            'Pluto': {'attack': 0.5, 'decay': 0.2, 'sustain': 1.0, 'release': 0.5}
        }
        
        envelope = planet_envelopes.get(planet, planet_envelopes['Sun']).copy()
        
        # Modify based on sign element
        element = self._get_sign_element(sign)
        element_modifiers = {
            'Fire': {'attack': 0.5, 'release': 0.5},
            'Earth': {'attack': 2.0, 'release': 2.0},
            'Air': {'attack': 0.7, 'release': 0.7},
            'Water': {'attack': 1.5, 'release': 1.5}
        }
        
        modifier = element_modifiers.get(element, {'attack': 1.0, 'release': 1.0})
        envelope['attack'] *= modifier['attack']
        envelope['release'] *= modifier['release']
        
        return envelope
    
    def _get_sign_element(self, sign: str) -> str:
        """Get element for a zodiac sign"""
        elements = {
            'Aries': 'Fire', 'Leo': 'Fire', 'Sagittarius': 'Fire',
            'Taurus': 'Earth', 'Virgo': 'Earth', 'Capricorn': 'Earth',
            'Gemini': 'Air', 'Libra': 'Air', 'Aquarius': 'Air',
            'Cancer': 'Water', 'Scorpio': 'Water', 'Pisces': 'Water'
        }
        return elements.get(sign, 'Earth')
    
    def _get_sign_quality(self, sign: str) -> str:
        """Get quality (modality) for a zodiac sign"""
        qualities = {
            'Aries': 'Cardinal', 'Cancer': 'Cardinal', 
            'Libra': 'Cardinal', 'Capricorn': 'Cardinal',
            'Taurus': 'Fixed', 'Leo': 'Fixed', 
            'Scorpio': 'Fixed', 'Aquarius': 'Fixed',
            'Gemini': 'Mutable', 'Virgo': 'Mutable', 
            'Sagittarius': 'Mutable', 'Pisces': 'Mutable'
        }
        return qualities.get(sign, 'Cardinal')
    
    def calculate_aspect_harmony(self, aspect_type: str, orb: float, 
                               planet1_freq: float, planet2_freq: float) -> Dict:
        """Calculate harmonic relationship between two planets"""
        # Get base interval for aspect
        aspect_intervals = {
            'conjunction': 'unison',
            'sextile': 'major_sixth',
            'square': 'minor_second',
            'trine': 'perfect_fifth',
            'opposition': 'octave',
            'quincunx': 'minor_seventh'
        }
        
        interval = aspect_intervals.get(aspect_type.lower(), 'unison')
        ratio = self.sacred_ratios[interval]
        
        # Calculate harmony frequency
        harmony_freq = planet1_freq * ratio
        
        # Orb affects the purity of the harmony
        orb_factor = 1 - (abs(orb) / 10)  # Closer orb = purer harmony
        
        # Calculate beat frequency (for subtle modulation)
        beat_freq = abs(planet2_freq - harmony_freq)
        
        return {
            'harmony_frequency': round(harmony_freq, 3),
            'beat_frequency': round(beat_freq, 3),
            'consonance': orb_factor,
            'interval_name': interval,
            'modulation_rate': round(beat_freq / 10, 3)  # Subtle modulation
        }
    
    def generate_musical_dna(self, full_chart_data: Dict) -> str:
        """Generate a unique musical DNA string for the chart"""
        # Create a unique identifier based on all planetary positions
        dna_components = []
        
        for planet, data in full_chart_data.items():
            if isinstance(data, dict) and 'frequency' in data:
                freq_int = int(data['frequency'] * 1000)
                dna_components.append(f"{planet[:2]}{freq_int}")
        
        # Add aspect signature
        aspect_signature = hashlib.md5(
            str(full_chart_data.get('aspects', [])).encode()
        ).hexdigest()[:8]
        
        dna_components.append(f"ASP{aspect_signature}")
        
        return "-".join(dna_components)


# Example usage and testing
if __name__ == "__main__":
    uniqueness = QuantumelodicUniqueness()
    
    # Test frequency calculation
    test_freq = uniqueness.calculate_unique_frequency(
        planet="Mars",
        sign="Scorpio",
        degree=15.5,
        minute=30,
        house=8
    )
    
    print("Mars in Scorpio Frequency Data:")
    print(f"Fundamental: {test_freq['fundamental']} Hz")
    print(f"Harmonics: {test_freq['harmonics']}")
    print(f"Rhythm Pattern: {test_freq['rhythm_pattern']}")
    print(f"Timbre: {test_freq['timbre_modifier']}")
    print(f"Envelope: {test_freq['amplitude_envelope']}")
    
    # Test aspect harmony
    aspect_harmony = uniqueness.calculate_aspect_harmony(
        aspect_type="trine",
        orb=2.5,
        planet1_freq=440.0,
        planet2_freq=660.0
    )
    
    print("\nTrine Aspect Harmony:")
    print(f"Harmony Frequency: {aspect_harmony['harmony_frequency']} Hz")
    print(f"Beat Frequency: {aspect_harmony['beat_frequency']} Hz")
    print(f"Consonance: {aspect_harmony['consonance']}")
