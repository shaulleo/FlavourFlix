import numpy as np
import pandas as pd
from currency_converter import CurrencyConverter
import datetime
import requests
from geopy.geocoders import Nominatim

#Find address from IP address
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
    
#Pre-processing of the restaurant schedule data
def clean_openinghours(observation):
    """Cleans the schedule of a given restaurant into a readable dictionary.
        Parameters:
        - observation (str): Opening hours of the restaurant.
        Returns:
        - opening_hours_dict (dict): Dictionary with the opening hours of the restaurant. """
    opening_hours_dict = {}
    for day in str(observation).split('\r\n'):
        day_week = f'{day.partition("y")[0]}y'
        opening_hours_dict[day_week] = day.partition("y")[2].strip()
        if opening_hours_dict[day_week] == '-':
            opening_hours_dict[day_week] = 'Closed'
        if day_week == 'y':
            del opening_hours_dict['y']
    return opening_hours_dict


#Checks if the restaurant is currently open
def check_if_open(restaurant_schedule):
    """Checks if a given restaurant is open at the current time.
        Parameters:
        - restaurant_schedule (dict): Opening hours of the restaurant.
        Returns:
        - open (str): 'Open' if the restaurant is open, 'Closed' otherwise. """
    
    current_date = datetime.date.today()
    day_of_week = current_date.strftime("%A")
    hour_format = "%H:%M"
    current_time = datetime.datetime.now().strftime(hour_format)
    current_time = datetime.datetime.strptime(current_time, hour_format).time()


    def check_schedule(schedule):
        opening_hours = schedule[:5]
        opening_hours = datetime.datetime.strptime(opening_hours, '%H:%M').time()
        closing_hours = schedule[-5:]
        if closing_hours == '24:00':
            closing_hours = '23:59'
        closing_hours = datetime.datetime.strptime(closing_hours, '%H:%M').time()
        if  (opening_hours <= current_time) & (current_time <= closing_hours):
            return True
        else:
            return False

    if restaurant_schedule[day_of_week] == 'Closed':
         return 'Closed'
    else:
        if "," not in restaurant_schedule[day_of_week]:
            open = check_schedule(restaurant_schedule[day_of_week].strip())
            if open:
                return 'Open'
        else:
            schedule = restaurant_schedule[day_of_week].partition(',')
            open1 = check_schedule(schedule[0].strip())
            open2 = check_schedule(schedule[-1].strip())
            if open1 or open2:
                 return 'Open'
    return 'Closed'


#Converts the average price of a restaurant to euros
def to_euros(row):
    """Converts the average price of a restaurant to euros.
        Parameters:
        - row (pandas.Series): Row of the dataframe.
        Returns:
        - euros (float): Average price of the restaurant in euros. """
    c = CurrencyConverter()
    if row['currency'] != 'EUR':
        euros = c.convert(row['averagePrice'], row['currency'], 'EUR')
    else:
        euros = row['averagePrice']
    return np.round(euros, 2)