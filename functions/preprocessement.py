import numpy as np
import pandas as pd
import datetime
import random
import re
import unicodedata
import requests
from functions.utils import *
from functions.env_colors import *
from functions.location import *



#Pre-processing of the restaurant schedule data
def clean_openinghours(observation):

    """Cleans the schedule of a given restaurant into a readable dictionary.
        Parameters:
        - observation (str): Opening hours of the restaurant.
        Returns:
        - opening_hours_dict (dict): Dictionary with the opening hours of the restaurant. """
    if observation == 'Not Available':
        return 'Not Available'
    else:   
        opening_hours_dict = {}
        for day in str(observation).split('\r\n'):
            day_week = f'{day.partition("y")[0]}y'
            opening_hours_dict[day_week] = day.partition("y")[2].strip()
            if opening_hours_dict[day_week] == '-':
                opening_hours_dict[day_week] = 'Closed'
            if day_week == 'y':
                del opening_hours_dict['y']
        return opening_hours_dict

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


def read_schedule_time(schedule, weekday):
    working_hours = []
    working_minutes = []
    schedule_time = schedule[weekday].split(',')
    for i in schedule_time:
        times = i.strip()
        working_hours.append(times[0:2])
        working_minutes.append(times[3:5])
        working_hours.append(times[8:10])
        working_minutes.append(times[11:13])

    return working_hours, working_minutes


def promotion_generator(schedule, prob):
    """Generates a promotion schedule for a restaurant.
        Parameters:
        - schedule (dict): Restaurant Schedule.
        - prob (float): Probability of a restaurant having a promotion.
        Returns:
        - promotion_schedules (list): List of restaurant's promotion type and schedule.
        """

    # Define the days of the week the restaurant is open.
    if type(schedule) == str:
        return 'No Offers'
    else:
        days_of_week = [key for key, value in schedule.items() if value != 'Closed']
        if days_of_week == []:
            return 'No Offers'

    # Define the promotion types
    promotion_types = ['Happy Hour', '10% off', '20% off','30% off', 'Free dessert', 'Free drink']

    if random.random() < prob:
        # Choose a random day of the week
        day_of_week = random.choice(days_of_week)
        # Choose a random promotion type
        promotion_type = random.choice(promotion_types)

        working_hours, working_minutes = read_schedule_time(schedule, day_of_week)
        
        # Define the promotion schedule
        if promotion_type == 'Happy Hour':
            start_time = f"{random.randint(6, 8)}:{random.choice(['00', '15', '30', '45'])}pm"
            end_time = f"{random.randint(9, 11)}:{random.choice(['00', '15', '30', '45'])}pm"
        elif promotion_type == '20% off':
            start_time = f"{random.randint(6, 8)}:{random.choice(['00', '15', '30', '45'])}pm"
            end_time = f"{random.randint(9, 11)}:{random.choice(['00', '15', '30', '45'])}pm"
        elif promotion_type == 'None':
            start_time = 'None'
            end_time = 'None'
        else:
            start_time = f"{random.randint(5, 7)}:{random.choice(['00', '15', '30', '45'])}pm"
            end_time = f"{random.randint(8, 10)}:{random.choice(['00', '15', '30', '45'])}pm"

            
        promo_info = {
                'promotion_type': promotion_type,
                'day_of_week': day_of_week,
                'start_time': start_time,
                'end_time': end_time,}


        return promo_info
    
    else:
        return 'No Offers'
    

def clean_chef_names(name):
    """Cleans the name of a chef.
        Parameters:
        - name (str): Name of the chef.
        Returns:
        - cleaned_name (str): Cleaned name of the chef. """
    
    if name == 'Not Applicable':
        return name
    else:
        #Remove unwanted terms from chef names
        expressions_to_remove = ['Chefes', 'Chefe', 'Chef', 'executivos', 'executivo', 'Pizzaiolo', 'Sommelier']
        pattern = '|'.join(re.escape(expr) for expr in expressions_to_remove)
        regex_pattern = re.compile(pattern, re.IGNORECASE)
        cleaned_name = regex_pattern.sub('', name)

        #Remove accents from chef names
        cleaned_name = unicodedata.normalize('NFKD', cleaned_name).encode('ascii', 'ignore').decode('utf-8')

        #Remove hashtags from chef names
        cleaned_name = re.sub(r'#\w*', '', cleaned_name)
        
        #Remove ponctuation from chef names
        cleaned_name = re.sub(r'[^\w\s]', '', cleaned_name)
        return cleaned_name.strip()
    

def get_chef_name(name):
    """Preprocesses the name of a chef.
        Parameters:
        - name (str): Name of the chef.
        Returns:
        - name (str or list): Preprocessed name of the chef. """
    name = re.split(r' e |, ', name)
    if len(name) == 1:
        name = clean_chef_names(str(name[0]))
    else:
        name = [clean_chef_names(str(x)) for x in name]
    return name


def preprocess_chefs(index, chef_list):
    if isinstance(chef_list, list) and len(chef_list) > index:
        return chef_list[index]
    else:
        if index == 0:
            return chef_list
        else:
            return 'Not Applicable'
        

def standardize_location(location):
    """Standardizes a location string.
        Parameters:
        - location (str): Location of the restaurant.
        Returns:
        - location (str): Standardized location of the restaurant."""

    #Tinha que ser...
    if location == 'Alamansil':
        location = 'Almancil'

    #remove abbreviations
    location = re.sub(r's\.', 'São', location, flags=re.IGNORECASE)
    location = re.sub(r'sta\.', 'Santa', location, flags=re.IGNORECASE)
    location = re.sub(r'q\.ta', 'Quinta', location, flags=re.IGNORECASE)

    return standardize_text(location)
