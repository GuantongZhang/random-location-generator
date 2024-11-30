import math
import random
from geopy.geocoders import Nominatim

# add as you need
boundaries = {
    'World': [90,-90,-180,180],
    'China': [53.6,18.1,73.5,135.1],
    'United States': [49.36,25.1,-124.76,-66.90],
    'Beijing': [41.07,39.42,115.40,117.54],
    }

geolocator = Nominatim(user_agent="GT")

def decdeg_to_dms(dd):
    degrees = int(dd)
    minutes = int((dd - degrees) * 60)
    seconds = (dd - degrees - minutes/60) * 3600
    return f"{degrees}° {minutes}' {seconds:.2f}\""

def generate_location(place, land_only=True, in_region_only=True, language="en", show_local_language=True):

    N,S,W,E = boundaries[place]
    DEG_TO_RAD = math.pi/180

    while True:
        longitude = random.uniform(W, E)

        a = N * DEG_TO_RAD
        b = S * DEG_TO_RAD

        # Ensures uniform distribution over the Earth's surface
        latitutde = math.asin(
            math.sin(b) + random.random()*(math.sin(a)-math.sin(b))
        ) / math.pi*180
        
        longitude_direction = "E" if longitude >= 0 else "W"
        latitutde_direction = "N" if latitutde >= 0 else "S"

        location = geolocator.reverse((latitutde, longitude), language="en")
        location_local_language = geolocator.reverse((latitutde, longitude))
        location_user_language = geolocator.reverse((latitutde, longitude), language=language)

        if location is None:  # address is not available
            if not land_only:
                print('Not on land.')
                break
            pass
        elif in_region_only and place != 'World' and place not in location.address:  # location is in other region
            pass
        else:
            print(f'Coordinate: {decdeg_to_dms(abs(latitutde))} {latitutde_direction}, {decdeg_to_dms(abs(longitude))} {longitude_direction}')
            print(f'Address: {location_user_language}')
            if show_local_language:
                print(f'         {location_local_language}')
            break

generate_location('China', language="en")
