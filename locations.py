from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from geopy.geocoders import Nominatim
import requests
import numpy as np
from env_colors import Color, TerminalTextColor



class Distance:
    """Class Distance: Defines an object representing the distance between two points.
    - Attributes:
        - km (float): Distance in kilometers.
        - meters (float): Distance in meters.
        - miles (float): Distance in miles.
        - minutes (int): Travel time in minutes.
        - hours (str): Travel time in hours and minutes.
    - Methods:
        - __init__(self, km=None, meters=None, miles = None, minutes=None, hours=None): Constructor of the class.
        - __str__(self): Description method of the class.
        
    """
    def __init__(self, km=None, meters=None, miles = None, minutes=None, hours=None):
        """ Class Constructor """
        self.km = km
        self.meters = meters
        self.miles = miles
        self.minutes = minutes
        self.hours = hours
    
    def __str__(self):
        """
        Prints the description of the Class Distance.
        """
        shift = "   "
        attributes = ""
        n_repeat = 80

        class_name = str(type(self)).split('.')[-1].replace("'>", "")

        print(
            f" 🗺️ Class: {TerminalTextColor.BLUE}{class_name}{TerminalTextColor.RESET}\n{'-' * n_repeat}")

        for k in self.__dict__:
            attributes += f"\n{shift}{shift}- {k}: {TerminalTextColor.BLUE}{self.__dict__[k]}{TerminalTextColor.RESET}"

        print(f"\n{shift}🏷️ Attributes: ")
        print(attributes)



        title = '- END -'
        print(f'\n{title}{"-" * (n_repeat-len(title))}')


class Location:
    """Class Location: Defines an object representing a location.
    - Attributes:
        - latitude (float): Latitude of the location.
        - longitude (float): Longitude of the location.
        - region (str): Region of the location.
        - city (str): City of the location.
    - Methods:
        - __init__(self, latitude=None, longitude=None, region=None, city=None): Constructor of the class.
        - getLocation(self): Gets the current location of the user.
        - getDirections(self, end_latitude, end_longitude, travel_modes): Gets the distance between the 
        location object and a given point.
        - __str__(self): Description method of the class.
    """

    def __init__(self, latitude=None, longitude=None, region=None, city=None):
        """ Class Constructor """
        self.latitude = latitude
        self.longitude = longitude
        self.region = region
        self.city = city
        self.__api_key = "AoqezzGOUEoJevKSMBGmvvseepc9ryhMu2YQkccOhaCKLXUG2snUIPxGkDNsRvYP"

    def getLocation(self):
        """ Gets the current location of the user. 
        Parameters:
        - None
        Returns:
        - None """
        #if self.latitude is None and self.longitude is None and self.region is None:
        options = Options()
        options.add_argument("--use--fake-ui-for-media-stream")
        driver = webdriver.Chrome()
        timeout = 20
        driver.get("https://mycurrentlocation.net/")
        wait = WebDriverWait(driver, timeout)
        time.sleep(20)

        self.latitude = driver.find_element(By.XPATH, '//*[@id="detail-latitude"]').text
        self.longitude = driver.find_element(By.XPATH, '//*[@id="detail-longitude"]').text
        self.region = driver.find_element(By.XPATH, '//*[@id="detail-location-name"]').text
        self.city = self.region.strip().split(',')[1]

        driver.quit()


    def getDirections(self, end_latitude, end_longitude, travel_modes):

        """ Gets the distance between the location object and a given point.
        Parameters:
        - end_latitude (float): Latitude of the end point.
        - end_longitude (float): Longitude of the end point.
        - travel_modes (str or list): Travel modes to be used in the calculation. can be either "walking", "driving" or "transit".
        Returns:
        - all_results (dict): Dictionary containing the distance and travel time between the two points for each travel mode.
        """

        if self.latitude is None or self.longitude is None:
            raise Exception("Location coordinates not found. Please run getLocation() first or specify initial point coordinates.")

        all_results = {}

        if type(travel_modes) == str:
            travel_modes = [travel_modes]

        for mode in travel_modes:
            base_url = "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix"
            params = {
                "origins": f"{self.latitude}, {self.longitude}",
                "destinations": f"{end_latitude},{end_longitude}",
                "travelMode": mode,
                "key": self.__api_key,
                "distanceUnit": "km",
                "timeUnit": "minute"
            }

            response = requests.get(base_url, params=params)

            if response.status_code == 200:
                data = response.json()

                if "resourceSets" in data and len(data["resourceSets"]) > 0:
                    resources = data["resourceSets"][0]["resources"]
                    if resources and len(resources) > 0:
                        result = resources[0]
                        travel_min = result["results"][0]["travelDuration"] #curretly in minutes
                        travel_km = result["results"][0]["travelDistance"] #currently in kms
                        
                        all_results[mode] = Distance(minutes = int(travel_min), 
                                                hours = f'{int(travel_min//60)}h{int(travel_min%60)}', 
                                                meters = np.round(travel_km*1000, 2),
                                                km = np.round(travel_km, 2),
                                                miles= np.round(travel_km/1.609, 2))
                        

                    else:
                        print(f"No results found for Travel Mode: {mode}")
                else:
                    print(f"No resources found for Travel Mode: {mode}")
            else:
                print(f"Request failed with status code {response.status_code} for Travel Mode: {mode}")
        
        if all_results == {}:
            return None
        else:
            return all_results
        

    def __str__(self):
        """
        Prints the description of the Class Location.
        """
        shift = "   "
        attributes = ""
        n_repeat = 80

        class_name = str(type(self)).split('.')[-1].replace("'>", "")

        print(
            f" 📍 Class: {TerminalTextColor.BLUE}{class_name}{TerminalTextColor.RESET}\n{'-' * n_repeat}")

        for k in self.__dict__:
            attributes += f"\n{shift}{shift}- {k}: {TerminalTextColor.BLUE}{self.__dict__[k]}{TerminalTextColor.RESET}"

        print(f"\n{shift}🏷️ Attributes: ")
        print(attributes)



        title = '- END -'
        print(f'\n{title}{"-" * (n_repeat-len(title))}')

        



            
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




