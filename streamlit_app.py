import json
from datetime import datetime

import pandas as pd
import streamlit as st

from utils.natal_csv_generator import (
    NatalInputs,
    build_csv_row,
    compute_natal_chart,
)

# Define the AstroEngine class
class AstroEngine:
    def __init__(self, chart_data):
        self.chart_data = chart_data
        self.dominant_element = self._calculate_dominant_element()
        self.aspect_patterns = self._identify_aspect_patterns()
        
    def _calculate_dominant_element(self):
        # Count elements across planets
        elements = {"Fire": 0, "Earth": 0, "Air": 0, "Water": 0}
        element_map = {
            "Aries": "Fire", "Leo": "Fire", "Sagittarius": "Fire",
            "Taurus": "Earth", "Virgo": "Earth", "Capricorn": "Earth",
            "Gemini": "Air", "Libra": "Air", "Aquarius": "Air",
            "Cancer": "Water", "Scorpio": "Water", "Pisces": "Water"
        }
        
        # Count elements for each planet
        for planet, data in self.chart_data["planets"].items():
            sign = data["sign"]
            if sign in element_map:
                elements[element_map[sign]] += 1
        
        # Return the element with highest count
        return max(elements, key=elements.get)
    
    def _identify_aspect_patterns(self):
        # Identify patterns from the aspects list
        patterns = []
        if "aspects" in self.chart_data and "majorAspects" in self.chart_data["aspects"]:
            aspects_text = " ".join(self.chart_data["aspects"]["majorAspects"])
            
            if "significantPatterns" in self.chart_data["aspects"]:
                if "trine" in aspects_text and "Grand Trine" in self.chart_data["aspects"]["significantPatterns"]:
                    patterns.append("Grand Trine")
                    
                if "square" in aspects_text and "T-Square" in self.chart_data["aspects"]["significantPatterns"]:
                    patterns.append("T-Square")
            
        return patterns
    
    def analyze_chart(self):
        # Full chart analysis
        return {
            "dominant_element": self.dominant_element,
            "aspect_patterns": self.aspect_patterns,
            "ascendant_influence": self.chart_data["angles"]["Ascendant"]["sign"] if "angles" in self.chart_data else "",
            "sun_moon_dynamic": f"{self.chart_data['planets']['Sun']['sign']}-{self.chart_data['planets']['Moon']['sign']}",
            "retrograde_planets": self._get_retrograde_planets()
        }
    
    def _get_retrograde_planets(self):
        # Return list of retrograde planets
        retrogrades = []
        for planet, data in self.chart_data["planets"].items():
            if "retrograde" in data and data["retrograde"]:
                retrogrades.append(planet)
        return retrogrades

# Define the MusicEngine class
class MusicEngine:
    def __init__(self):
        # Define musical mappings
        self.planet_to_mode = {
            "Sun": {"mode": "Ionian", "tonic": "E", "instrument": "Brass", "tempo": 120},
            "Moon": {"mode": "Aeolian", "tonic": "F", "instrument": "Piano, Cello", "tempo": 70},
            "Mercury": {"mode": "Mixolydian", "tonic": "D", "instrument": "Flutes", "tempo": 130},
            "Venus": {"mode": "Lydian", "tonic": "G", "instrument": "Strings", "tempo": 70},
            "Mars": {"mode": "Phrygian", "tonic": "C", "instrument": "Percussion", "tempo": 160},
            "Jupiter": {"mode": "Lydian", "tonic": "A", "instrument": "Brass", "tempo": 100},
            "Saturn": {"mode": "Dorian", "tonic": "B", "instrument": "Bassoon", "tempo": 60},
            "Uranus": {"mode": "Aeolian", "tonic": "Ab", "instrument": "Synthesizers", "tempo": 140},
            "Neptune": {"mode": "Ionian", "tonic": "Bb", "instrument": "Harp", "tempo": 50},
            "Pluto": {"mode": "Phrygian", "tonic": "Db", "instrument": "Low Brass", "tempo": 90}
        }
        
        self.aspect_to_harmony = {
            "conjunction": "Unison",
            "trine": "Perfect Fifth",
            "square": "Tritone",
            "opposition": "Octave",
            "sextile": "Major Third"
        }
        
        self.house_to_form = {
            "1": "Introduction",
            "4": "Emotional Theme",
            "7": "Balance Section",
            "10": "Climactic Section"
        }
    
    def generate_melody(self, planet, sign):
        # Generate a melodic theme based on planet and sign
        if planet not in self.planet_to_mode:
            return {"mode": "Ionian", "tonic": "C", "tempo": 120, "quality": "Neutral", "instrument": "Piano"}
            
        planet_data = self.planet_to_mode[planet]
        
        # Adjust for sign influence (simplified)
        sign_groups = {
            "Fire": {"tempo_mod": 1.2, "intensity": "Strong"},
            "Earth": {"tempo_mod": 0.9, "intensity": "Steady"},
            "Air": {"tempo_mod": 1.1, "intensity": "Light"},
            "Water": {"tempo_mod": 0.8, "intensity": "Flowing"}
        }
        
        element_map = {
            "Aries": "Fire", "Leo": "Fire", "Sagittarius": "Fire",
            "Taurus": "Earth", "Virgo": "Earth", "Capricorn": "Earth",
            "Gemini": "Air", "Libra": "Air", "Aquarius": "Air",
            "Cancer": "Water", "Scorpio": "Water", "Pisces": "Water"
        }
        
        element = element_map.get(sign, "Fire")
        sign_influence = sign_groups[element]
        
        # Create melody template
        melody = {
            "mode": planet_data["mode"],
            "tonic": planet_data["tonic"],
            "tempo": planet_data["tempo"] * sign_influence["tempo_mod"],
            "quality": sign_influence["intensity"],
            "instrument": planet_data["instrument"]
        }
        
        return melody
    
    def generate_harmony(self, aspects):
        # Generate harmonic progression based on aspects
        harmonies = []
        
        # Simple implementation
        for aspect in aspects:
            for aspect_type, harmony in self.aspect_to_harmony.items():
                if aspect_type in aspect.lower():
                    harmonies.append(harmony)
                    break
        
        return harmonies
    
    def generate_form(self, houses):
        # Generate musical form based on house placements
        form_sections = []
        
        for house, form in self.house_to_form.items():
            if house in houses:
                form_sections.append(form)
        
        # Add default sections if needed
        if not form_sections:
            form_sections = ["Introduction", "Development", "Conclusion"]
            
        return form_sections

# Define the MappingEngine class
class MappingEngine:
    def __init__(self, astro_engine, music_engine):
        self.astro_engine = astro_engine
        self.music_engine = music_engine
    
    def translate_chart(self):
        # Analyze the chart
        chart_analysis = self.astro_engine.analyze_chart()
        
        # Generate musical elements
        sun_melody = self.music_engine.generate_melody(
            "Sun", 
            self.astro_engine.chart_data["planets"]["Sun"]["sign"]
        )
        
        moon_melody = self.music_engine.generate_melody(
            "Moon", 
            self.astro_engine.chart_data["planets"]["Moon"]["sign"]
        )
        
        # Generate dominant harmonies
        harmonies = []
        if "aspects" in self.astro_engine.chart_data and "majorAspects" in self.astro_engine.chart_data["aspects"]:
            harmonies = self.music_engine.generate_harmony(
                self.astro_engine.chart_data["aspects"]["majorAspects"]
            )
        
        # Generate form structure
        houses = [data["house"] for planet, data in self.astro_engine.chart_data["planets"].items()]
        form = self.music_engine.generate_form(houses)
        
        # Adjust for retrograde planets
        retrogrades = chart_analysis["retrograde_planets"]
        retrograde_effects = [f"{planet} melody reversed" for planet in retrogrades]
        
        # Create composition structure
        composition = {
            "title": self._generate_title(chart_analysis),
            "overview": self._generate_overview(chart_analysis, sun_melody, moon_melody),
            "structure": form,
            "musical_details": {
                "key": self._determine_key(self.astro_engine.chart_data["angles"]["Ascendant"]["sign"] if "angles" in self.astro_engine.chart_data else "Aries"),
                "time_signature": self._determine_time_signature(chart_analysis["dominant_element"]),
                "tempo": self._calculate_average_tempo(sun_melody, moon_melody),
                "melodies": {
                    "sun_theme": sun_melody,
                    "moon_theme": moon_melody
                },
                "harmonies": harmonies,
                "retrograde_effects": retrograde_effects
            },
            "instrumentation": self._determine_instrumentation(chart_analysis),
            "performance_notes": self._generate_performance_notes(chart_analysis)
        }
        
        return composition
    
    def _generate_title(self, analysis):
        # Generate a title based on chart elements
        return f"Cosmic Symphony in {analysis['dominant_element']} - {analysis['ascendant_influence']} Ascension"
    
    def _generate_overview(self, analysis, sun_melody, moon_melody):
        # Generate overview text
        minutes = 5 + len(analysis["aspect_patterns"])  # Simple duration calculation
        return f"A {minutes}-minute composition exploring the {analysis['sun_moon_dynamic']} dynamic, with {analysis['dominant_element']} element dominating the piece. Tempo averages {int(self._calculate_average_tempo(sun_melody, moon_melody))} BPM."
    
    def _determine_key(self, ascendant):
        # Map ascendant to musical key
        key_map = {
            "Aries": "C Major", "Leo": "G Major", "Sagittarius": "D Major",
            "Taurus": "F Major", "Virgo": "Bb Major", "Capricorn": "Eb Major",
            "Gemini": "A Major", "Libra": "E Major", "Aquarius": "B Major",
            "Cancer": "D Minor", "Scorpio": "G Minor", "Pisces": "C Minor"
        }
        return key_map.get(ascendant, "C Major")
    
    def _determine_time_signature(self, element):
        # Map element to time signature
        sig_map = {
            "Fire": "4/4", "Earth": "4/4", 
            "Air": "3/4", "Water": "6/8"
        }
        return sig_map.get(element, "4/4")
    
    def _calculate_average_tempo(self, sun_melody, moon_melody):
        # Simple averaging of Sun and Moon tempos
        return (sun_melody["tempo"] + moon_melody["tempo"]) / 2
    
    def _determine_instrumentation(self, analysis):
        # Determine instrumentation based on chart analysis
        instruments = []
        
        if analysis["dominant_element"] == "Fire":
            instruments.extend(["Brass", "Percussion", "Electric Guitar"])
        elif analysis["dominant_element"] == "Earth":
            instruments.extend(["Strings", "Bass", "Acoustic Guitar"])
        elif analysis["dominant_element"] == "Air":
            instruments.extend(["Woodwinds", "Synthesizer", "Harp"])
        elif analysis["dominant_element"] == "Water":
            instruments.extend(["Piano", "Cello", "Ambient Synths"])
            
        return instruments
    
    def _generate_performance_notes(self, analysis):
        # Generate performance guidance
        element_qualities = {
            "Fire": "energetic and bold, with strong dynamics and assertive articulation",
            "Earth": "grounded and steady, with consistent rhythm and rich tonal quality",
            "Air": "light and fluid, with agile phrasing and transparent textures",
            "Water": "flowing and emotional, with rubato and expressive dynamics"
        }
        
        return f"Perform with a {element_qualities[analysis['dominant_element']]} character. {', '.join(analysis['aspect_patterns']) if analysis['aspect_patterns'] else 'Focus on the melodic interplay between themes'}."

# Streamlit App
st.set_page_config(
    page_title="Quantumelodic MetaSystem",
    page_icon="🎵",
    layout="wide"
)

st.title("Quantumelodic MetaSystem")
st.subheader("Generate musical compositions from astrological data")

st.markdown("---")
st.header("Natal Chart CSV Builder")

with st.form("natal_csv_form"):
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        full_name = st.text_input("Name", value="Cosmic Explorer")
        csv_birth_date = st.date_input("Birth Date", key="csv_birth_date")
        timezone_str = st.text_input("Time Zone (e.g., America/New_York)", value="UTC")
    with col_b:
        csv_birth_time = st.time_input("Birth Time", key="csv_birth_time")
        latitude = st.number_input("Latitude", format="%0.6f", value=0.0)
        longitude = st.number_input("Longitude", format="%0.6f", value=0.0)
    with col_c:
        st.markdown(
            "Provide the precise birth coordinates and time zone for the most accurate chart."
        )
        st.markdown(
            "The resulting CSV row follows the requested schema and can be downloaded directly."
        )

    submitted = st.form_submit_button("Generate Natal CSV Row", type="primary")

if submitted:
    try:
        birth_dt = datetime.combine(csv_birth_date, csv_birth_time)
        natal_inputs = NatalInputs(
            name=full_name,
            birth_datetime=birth_dt,
            latitude=latitude,
            longitude=longitude,
            timezone=timezone_str,
        )

        planetary_chart = compute_natal_chart(natal_inputs)
        csv_row = build_csv_row(planetary_chart, natal_inputs)

        st.success("Natal chart synthesized successfully!")
        display_df = pd.DataFrame([csv_row])
        st.dataframe(display_df, use_container_width=True)

        csv_bytes = display_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV Row",
            data=csv_bytes,
            file_name="natal_chart_row.csv",
            mime="text/csv",
        )

        with st.expander("Planetary Positions", expanded=False):
            st.json(planetary_chart)

    except Exception as e:
        st.error(
            "Unable to compute the natal chart automatically. Ensure latitude, longitude, time zone, and ephemeris data are available."
        )
        st.exception(e)

with st.container():
    st.markdown("## Birth Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        birth_date = st.date_input("Birth Date")
    with col2:
        birth_time = st.time_input("Birth Time")
    with col3:
        birth_location = st.text_input("Birth Location (City, Country)")

# Planet input section
planets_data = {}
with st.expander("Planetary Positions", expanded=True):
    planet_names = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
    zodiac_signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    houses = [str(i) for i in range(1, 13)]
    
    # Create 2 rows of 5 planets each
    rows = [planet_names[i:i+5] for i in range(0, len(planet_names), 5)]
    
    for row in rows:
        cols = st.columns(5)
        for i, planet in enumerate(row):
            with cols[i]:
                st.markdown(f"**{planet}**")
                sign = st.selectbox(f"{planet} Sign", zodiac_signs, key=f"{planet}_sign")
                degree = st.number_input(f"{planet} Degree", min_value=0.0, max_value=29.99, step=0.01, key=f"{planet}_degree")
                house = st.selectbox(f"{planet} House", houses, key=f"{planet}_house")
                retrograde = st.checkbox(f"{planet} Retrograde", key=f"{planet}_retrograde")
                
                planets_data[planet] = {
                    "sign": sign,
                    "degree": degree,
                    "house": house,
                    "retrograde": retrograde
                }

# Ascendant and Midheaven
with st.expander("Ascendant & Midheaven", expanded=True):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        asc_sign = st.selectbox("Ascendant Sign", zodiac_signs)
    with col2:
        asc_degree = st.number_input("Ascendant Degree", min_value=0.0, max_value=29.99, step=0.01)
    with col3:
        mc_sign = st.selectbox("Midheaven Sign", zodiac_signs)
    with col4:
        mc_degree = st.number_input("Midheaven Degree", min_value=0.0, max_value=29.99, step=0.01)

# Chart information
with st.expander("Chart Information", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        house_system = st.selectbox("House System", ["Placidus", "Whole Sign", "Equal", "Koch", "Porphyry", "Regiomontanus", "Campanus"])
        chart_shape = st.selectbox("Chart Shape", ["", "Bundle", "Bowl", "Bucket", "Seesaw", "Splash", "Locomotive"])
    with col2:
        dominant_element = st.selectbox("Dominant Element", ["", "Fire", "Earth", "Air", "Water"])
        dominant_mode = st.selectbox("Dominant Mode", ["", "Cardinal", "Fixed", "Mutable"])

# Aspects & Patterns
with st.expander("Aspects & Patterns", expanded=True):
    major_aspects = st.text_area("Major Aspects (One per line)", 
                                height=150, 
                                help="Enter aspects like 'Sun trine Moon', 'Venus square Mars', etc.")
    
    significant_patterns = st.multiselect("Significant Patterns", 
                                        ["Grand Trine", "T-Square", "Grand Cross", "Yod", "Stellium", 
                                        "Mystic Rectangle", "Kite", "Grand Sextile", "Double Grand Trine"])
    
    stellium_details = st.text_input("Stellium Details (if applicable)", 
                                   placeholder="e.g., 'Stellium in Taurus (Venus, Mercury, Mars)'")

# Additional notes
with st.expander("Additional Notes", expanded=False):
    notable_features = st.text_area("Notable Features", 
                                  placeholder="Any other notable features of the chart (e.g., unaspected planets, intercepted signs, etc.)")

# Generate composition button
if st.button("Generate Quantumelodic Composition", type="primary"):
    with st.spinner("Generating cosmic composition..."):
        # Format the data
        chart_data = {
            "birthInfo": {
                "date": birth_date.strftime("%Y-%m-%d"),
                "time": birth_time.strftime("%H:%M"),
                "location": birth_location
            },
            "planets": planets_data,
            "angles": {
                "Ascendant": {
                    "sign": asc_sign,
                    "degree": asc_degree
                },
                "Midheaven": {
                    "sign": mc_sign,
                    "degree": mc_degree
                }
            },
            "chartInfo": {
                "houseSystem": house_system,
                "chartShape": chart_shape,
                "dominantElement": dominant_element,
                "dominantMode": dominant_mode
            },
            "aspects": {
                "majorAspects": major_aspects.split('\n') if major_aspects else [],
                "significantPatterns": significant_patterns,
                "stelliumDetails": stellium_details
            },
            "notes": {
                "notableFeatures": notable_features
            }
        }
        
        # Process through the Quantumelodic MetaSystem
        astro_engine = AstroEngine(chart_data)
        music_engine = MusicEngine()
        mapping_engine = MappingEngine(astro_engine, music_engine)
        
        # Generate the composition
        try:
            composition = mapping_engine.translate_chart()
            
            # Display composition
            st.success("Composition generated successfully!")
            
            # Title and Overview
            st.markdown(f"## {composition['title']}")
            st.markdown(f"*{composition['overview']}*")
            
            # Composition details in columns
            col1, col2 = st.columns(2)
            
            # Column 1: Structure and Musical Details
            with col1:
                st.markdown("### Structure")
                for i, section in enumerate(composition['structure']):
                    st.markdown(f"{i+1}. {section}")
                
                st.markdown("### Musical Details")
                st.markdown(f"**Key:** {composition['musical_details']['key']}")
                st.markdown(f"**Time Signature:** {composition['musical_details']['time_signature']}")
                st.markdown(f"**Tempo:** {int(composition['musical_details']['tempo'])} BPM")
                
                st.markdown("#### Melodic Themes")
                st.markdown(f"**Sun Theme:** {composition['musical_details']['melodies']['sun_theme']['mode']} mode in {composition['musical_details']['melodies']['sun_theme']['tonic']}, played at {composition['musical_details']['melodies']['sun_theme']['tempo']:.1f} BPM with {composition['musical_details']['melodies']['sun_theme']['quality']} character on {composition['musical_details']['melodies']['sun_theme']['instrument']}")
                st.markdown(f"**Moon Theme:** {composition['musical_details']['melodies']['moon_theme']['mode']} mode in {composition['musical_details']['melodies']['moon_theme']['tonic']}, played at {composition['musical_details']['melodies']['moon_theme']['tempo']:.1f} BPM with {composition['musical_details']['melodies']['moon_theme']['quality']} character on {composition['musical_details']['melodies']['moon_theme']['instrument']}")
            
            # Column 2: Harmonic Progressions, Instrumentation and Performance Notes
            with col2:
                st.markdown("### Harmonic Progressions")
                if composition['musical_details']['harmonies']:
                    for harmony in composition['musical_details']['harmonies']:
                        st.markdown(f"- {harmony}")
                else:
                    st.markdown("Simple diatonic progressions")
                
                if composition['musical_details']['retrograde_effects']:
                    st.markdown("#### Special Effects")
                    for effect in composition['musical_details']['retrograde_effects']:
                        st.markdown(f"- {effect}")
                
                st.markdown("### Instrumentation")
                for instrument in composition['instrumentation']:
                    st.markdown(f"- {instrument}")
                
                st.markdown("### Performance Notes")
                st.markdown(composition['performance_notes'])
            
            # Debug: show raw data
            with st.expander("Raw Data (Debug)", expanded=False):
                st.json(composition)
                
        except Exception as e:
            st.error(f"Error generating composition: {str(e)}")
            st.write("Please check your input data and try again.")
