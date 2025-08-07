from skyfield.api import Topos, load
from datetime import datetime
import pytz

def ra_to_zodiac_sign(ra_hours, ra_minutes, ra_seconds):
    degrees = ra_hours * 15 + ra_minutes * 0.25 + ra_seconds * 0.004167
    if 0 <= degrees < 30:
        return "Aries", degrees
    elif 30 <= degrees < 60:
        return "Taurus", degrees - 30
    elif 60 <= degrees < 90:
        return "Gemini", degrees - 60
    elif 90 <= degrees < 120:
        return "Cancer", degrees - 90
    elif 120 <= degrees < 150:
        return "Leo", degrees - 120
    elif 150 <= degrees < 180:
        return "Virgo", degrees - 150
    elif 180 <= degrees < 210:
        return "Libra", degrees - 180
    elif 210 <= degrees < 240:
        return "Scorpio", degrees - 210
    elif 240 <= degrees < 270:
        return "Sagittarius", degrees - 240
    elif 270 <= degrees < 300:
        return "Capricorn", degrees - 270
    elif 300 <= degrees < 330:
        return "Aquarius", degrees - 300
    elif 330 <= degrees < 360:
        return "Pisces", degrees - 330

def get_planetary_positions(date_time, location):
    planets = load('de421.bsp')
    ts = load.timescale()
    
    t = ts.utc(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second)

    positions = {
        "Sun": planets['sun'].at(t).observe(planets['earth']).apparent(),
        "Moon": planets['moon'].at(t).observe(planets['earth']).apparent(),
        "Mercury": planets['mercury'].at(t).observe(planets['earth']).apparent(),
        "Venus": planets['venus'].at(t).observe(planets['earth']).apparent(),
        "Mars": planets['mars'].at(t).observe(planets['earth']).apparent(),
        "Jupiter": planets['jupiter barycenter'].at(t).observe(planets['earth']).apparent(),
        "Saturn": planets['saturn barycenter'].at(t).observe(planets['earth']).apparent(),
        "Uranus": planets['uranus barycenter'].at(t).observe(planets['earth']).apparent(),
        "Neptune": planets['neptune barycenter'].at(t).observe(planets['earth']).apparent(),
        "Pluto": planets['pluto barycenter'].at(t).observe(planets['earth']).apparent()
    }

    planetary_ra = {}
    for planet, position in positions.items():
        ra, dec, distance = position.radec()
        ra_hours = ra.hours
        ra_minutes = ra.minutes
        ra_seconds = ra.seconds
        planetary_ra[planet] = (ra_hours, ra_minutes, ra_seconds)
    
    return planetary_ra

def main():
    # Input date and time
    date_time_str = input("Enter date and time (YYYY-MM-DD HH:MM:SS): ")
    date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

    # Convert local time to UTC
    timezone = pytz.timezone('America/New_York')
    date_time_utc = timezone.localize(date_time).astimezone(pytz.utc)

    # Get planetary positions
    planetary_ra = get_planetary_positions(date_time_utc, Topos('40.7128 N', '74.0060 W'))

    # Convert RA to Zodiac Signs
    zodiac_positions = {planet: ra_to_zodiac_sign(*ra) for planet, ra in planetary_ra.items()}
    
    for planet, (sign, degrees) in zodiac_positions.items():
        print(f'{planet}: {sign} {degrees:.2f}°')

if __name__ == "__main__":
    main()
