import requests

def get_coordinates(place_name):
    api_key = 'YOUR_OPENCAGE_API_KEY'  # Replace with your actual key
    url = f'https://api.opencagedata.com/geocode/v1/json?q={place_name}&key={api_key}'
    response = requests.get(url)
    data = response.json()

    if data['results']:
        loc = data['results'][0]['geometry']
        return loc['lat'], loc['lng']
    return None, None
