import streamlit as st
from datetime import datetime
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const

def validate_input(date_str, time_str, timezone_str, lat, lon):
    errors = []
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        errors.append("Birthdate must be in YYYY-MM-DD format.")
    try:
        datetime.strptime(time_str, "%H:%M")
    except ValueError:
        errors.append("Birth time must be in HH:MM 24-hour format.")
    if not (timezone_str.startswith('+') or timezone_str.startswith('-')) or len(timezone_str) != 6:
        errors.append("Timezone must be in format +00:00 or -05:00.")
    if not lat or not lon:
        errors.append("Latitude and Longitude must be filled in.")
    return errors

def generate_chart_data(birth_date, birth_time, timezone, lat, lon):
    dt = Datetime(date=birth_date, time=birth_time, utcoffset=timezone)
    pos = GeoPos(lat, lon)
    chart = Chart(dt, pos)
    planets = {}
    for obj in chart.objects:
        if obj in [const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
                   const.JUPITER, const.SATURN, const.URANUS, const.NEPTUNE, const.PLUTO]:
            planets[obj] = {"sign": chart.get(obj).sign, "degree": chart.get(obj).lon}
    return {"planets": planets}

def generate_quantumelodic_profile(chart_data):
    tones = []
    base_note = 60
    for planet, data in chart_data['planets'].items():
        degree = data['degree']
        try:
            midi_note = int(base_note + (float(degree) / 30.0) * 12)
            tones.append(midi_note)
        except:
            tones.append(base_note)
    return tones

def render_midi(melody_sequence, filename="quantumelodic_output.mid"):
    from music21 import stream, note, midi
    s = stream.Stream()
    for pitch in melody_sequence:
        n = note.Note()
        n.pitch.midi = pitch
        n.quarterLength = 1
        s.append(n)
    mf = midi.translate.streamToMidiFile(s)
    mf.open(filename, 'wb')
    mf.write()
    mf.close()

def main():
    st.title("Quantumelodic Music Generator")

    st.subheader("Birth Information")
    birth_date = st.text_input("Birthdate (YYYY-MM-DD)", value="1985-04-24")
    birth_time = st.text_input("Birth Time (HH:MM)", value="18:46")
    timezone = st.text_input("Timezone (e.g., +00:00)", value="+00:00")

    st.subheader("Geographic Coordinates")
    lat = st.text_input("Latitude (e.g., 40n42)", value="40n42")
    lon = st.text_input("Longitude (e.g., 74w00)", value="74w00")

    if st.button("Generate Music"):
        errors = validate_input(birth_date, birth_time, timezone, lat, lon)
        if errors:
            for error in errors:
                st.error(error)
        else:
            try:
                chart_data = generate_chart_data(birth_date, birth_time, timezone, lat, lon)
                melody = generate_quantumelodic_profile(chart_data)
                render_midi(melody, "quantumelodic_output.mid")
                st.success("Music generated successfully!")
                st.audio("quantumelodic_output.mid")

                st.subheader("Planetary Mapping")
                for planet, data in chart_data["planets"].items():
                    st.write(f"{planet}: {data['sign']} at {round(data['degree'], 2)}°")

            except Exception as e:
                st.error(f"Critical error: {e}")

if __name__ == "__main__":
    main()