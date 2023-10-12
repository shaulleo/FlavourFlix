from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from geopy.geocoders import Nominatim


class Location:
    """This class is used to get the location of the user"""

    def __init__(self, latitude = None, longitude = None, region = None, city=None):
        self.latitude = latitude
        self.longitude = longitude
        self.region = region
        self.city = None

    def getLocation(self):
        options = Options()
        options.add_argument("--use--fake-ui-for-media-stream")
        driver = webdriver.Chrome()
        timeout = 20
        driver.get("https://mycurrentlocation.net/")
        wait = WebDriverWait(driver, timeout)
        time.sleep(20)

        self.longitude = str(driver.find_element(By.XPATH, '//*[@id="detail-latitude"]').text)
        self.latitude = str(driver.find_element(By.XPATH, '//*[@id="detail-longitude"]').text)
        self.region = str(driver.find_element(By.XPATH, '//*[@id="detail-location-name"]').text)
        self.city = self.region.split(',')[0]
        driver.quit()

# -------------------- This fuction is not used in the project --------------------
#Find address from IP address
#Restaurants in your city.
def find_my_address():
    """Find address from IP address
        Parameters:
        - None
        Returns:
        - address (str): Address of the user"""

    try:
        # Make a request to ipinfo.io to get location details based on your IP address
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        
        if "loc" in data:
            # Extract latitude and longitude from the 'loc' field
            latitude, longitude = map(float, data["loc"].split(","))

            geolocator = Nominatim(user_agent="myGeocoder")
            location = geolocator.reverse((latitude, longitude), exactly_one=True)

            if location:
                address = location.address
                return address
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    

def preprocess_address(address):
    """Preprocesses the address of a restaurant.
        Parameters:
        - address (str): Address of the restaurant.
        Returns:
        - address (str): Preprocessed address of the restaurant. """
    #Add a whitespace after every comma in the address column
    address = address.replace(',', ',')
    #Remove the second last value in the address (postal code)
    address = address.split(',')
    address.remove(address[-2])
    #Add Portugal to the address list
    address.append(' Portugal')
    #Join the address list into a string
    address = ','.join(address)
    return address



def find_coordinates(address):
    """Find latitude and longitude coordinates from address using Bing Maps API
        Parameters:
        - address (str): Address of the restaurant.
        Returns:
        - latitude (float): Latitude of the restaurant.
        - longitude (float): Longitude of the restaurant. """
    
    # Replace 'YOUR_BING_MAPS_API_KEY' with your actual API key
    api_key = 'AoqezzGOUEoJevKSMBGmvvseepc9ryhMu2YQkccOhaCKLXUG2snUIPxGkDNsRvYP'

    # Define the API endpoint and parameters
    base_url = 'http://dev.virtualearth.net/REST/v1/Locations'
    params = {
        'q': address,
        'key': api_key,
    }

    # Make the API request
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Extract the coordinates (latitude and longitude) from the response
        if 'resourceSets' in data and data['resourceSets'] and 'resources' in data['resourceSets'][0]:
            location = data['resourceSets'][0]['resources'][0]
            latitude = location['point']['coordinates'][0]
            longitude = location['point']['coordinates'][1]

            return latitude, longitude
        else:
            print("No location data found in the response.")
            latitude = None
            longitude = None
    else:
        print("Error making API request:", response.status_code, response.text)
        latitude = None
        longitude = None
    
    return latitude, longitude