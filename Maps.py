# Maps.py

import requests

### global
BASE_URL = "https://maps.googleapis.com/maps/api/staticmap?"
API_KEY = "AIzaSyAHPLtWASmFGFF5bbPGBVEjXwafsagQbxs"
ZOOM = 16

class GMap():
    def getMap(self, lat, logt):
        URL = BASE_URL + "size=305x315" + "&markers=color:blue%7C" + lat + "," + logt + "&key=" + API_KEY
        response = requests.get(URL)
        with open('map.png', 'wb') as file:
            file.write(response.content)



