import requests

def query_location(location, categories):
    """
    Queries from Facebook Places API given a location, and a list of
    categories. Returns the Place with the most checkins, which is assumed
    to be the most popular.
    """
    ACCESS_TOKEN = YOUR_ACCESS_TOKEN
    FB_PARAMS = {'categories' : str(categories), \
        'fields': ['name,checkins,overall_star_rating,location,price_range'], \
        'q': location, \
        'access_token': ACCESS_TOKEN}
    res = requests.get(url = FB_URL, params = FB_PARAMS)
    all_locations = res.json()['data']
    all_locations.sort(key = lambda place: -place['checkins'])
    return all_locations[0]['name']
