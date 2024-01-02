import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
import re
import unicodedata
import requests
from functions.utils import *
from functions.env_colors import *
from functions.location import *
#from functions.utils import standardize_text

# ------------------------------- Restaurant Data Preprocessing ------------------------------

def clean_openinghours(observation: str):
    """Cleans the schedule of a given restaurant into a readable dictionary.
    Parameters:
        - observation (str): Opening hours of the restaurant.
     Returns:
        - opening_hours_dict (dict): Dictionary with the opening hours of the restaurant. """
    
    if observation == 'Not Available':
        return 'Not Available'
    else:   
        opening_hours_dict = {}

        #Split the schedule by day
        for day in str(observation).split('\r\n'):
            #Remove unwanted characters
            day_week = f'{day.partition("y")[0]}y'
            opening_hours_dict[day_week] = day.partition("y")[2].strip()
            #Verify if restaurant is closed
            if opening_hours_dict[day_week] == '-':
                opening_hours_dict[day_week] = 'Closed'
            temp = opening_hours_dict[day_week].split(',')
            # Correct midnight to 23:59
            temp = [i.replace('24:00', '23:59') for i in temp]
            temp = ','.join(temp)
            opening_hours_dict[day_week] = temp

            #Remove unwanted characters
            if day_week == 'y':
                del opening_hours_dict['y']
        return opening_hours_dict


def preprocess_address(address: str):
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


def find_coordinates(address: str):
    """Find latitude and longitude coordinates from address using Bing Maps API
    Parameters:
        - address (str): Address of the restaurant.
    Returns:
        - latitude (float): Latitude of the restaurant.
        - longitude (float): Longitude of the restaurant. """

    #Define the API endpoint and parameters
    params = {
        'q': address,
        'key': local_settings.COORDINATES_API,
    }

    #Make the API request
    response = requests.get(local_settings.COORDINATES_BASE_URL, params=params)

    #Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        #Extract the coordinates (latitude and longitude) from the response
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


def find_random_time(time_string:str, start=True):
    """Finds a random time within a given time range.
    Parameters:
        - time_string (str): Time range.
        - start (bool): Whether the random time should be the start or end of the time range.
    Returns: 
        - random_time_str (str): Random time within the provided time range."""

    start_time_str, end_time_str = time_string.split(" - ")

    #Define format for parsing time
    time_format = "%H:%M"

    # Parse the start and end times
    start_time = datetime.datetime.strptime(start_time_str.strip(), time_format)
    end_time = datetime.datetime.strptime(end_time_str.strip(), time_format)

    if start == True:
        #Ensure the random time is at least 1 hour earlier than closing hour
        min_time = start_time 
        max_time = end_time  - timedelta(hours=1)
    else:
        #Ensure the random time is at least 15 minutes earlier than closing hour
        min_time = start_time 
        max_time = end_time - timedelta(minutes= 15)

    #Calculate the time difference in minutes
    time_diff_minutes = (max_time - min_time).total_seconds() / 60

    #Calculate the number of quarter-hour intervals within the time range
    num_intervals = int(time_diff_minutes / 15)

    #Generate a random number of quarter-hour intervals to subtract
    random_intervals = random.randint(0, num_intervals)

    # Calculate the random time
    random_time = min_time + timedelta(minutes=random_intervals * 15)

    # Format the random time as a string
    random_time_str = random_time.strftime("%H:%M")

    return random_time_str


def promotion_generator(schedule: dict, prob:float):
    """Generates a promotion schedule for a restaurant.
    Parameters:
        - schedule (dict): Restaurant Schedule.
        - prob (float): Probability of a restaurant having a promotion.
    Returns:
        - promotion_schedules (dict): Information about the restaurant's promotional offers.
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
        try:
            # Choose a random day of the week
            day_of_week = random.choice(days_of_week)
            # Choose a random promotion type
            promotion_type = random.choice(promotion_types)

            schedule_time = schedule[day_of_week].split(',')

            # Define the promotion schedule
            if promotion_type == 'Happy Hour' or  promotion_type == '20% off' or promotion_type == '30% off':
                start_time = find_random_time(schedule_time[0], start=True)
                end_time =  find_random_time(schedule_time[0], start=False)        
            else:
                if len(schedule_time) > 1:
                    start_time = find_random_time(schedule_time[1], start=True)
                    end_time =  find_random_time(schedule_time[1], start=False)
                else:
                    start_time = find_random_time(schedule_time[0], start=True)
                    end_time =  find_random_time(schedule_time[0], start=False)

            #Store all promotion info in a dictionary
            promo_info = {
                    'promotion_type': promotion_type,
                    'day_of_week': day_of_week,
                    'start_time': start_time,
                    'end_time': end_time,}

            return promo_info    
        except ValueError as v:
            return 'No Offers'
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
    

def get_chef_name(name:str):
    """Separates the names of the chefs.
    Parameters:
        - name (str): Name of the chef.
    Returns:
        - name (str or list): Name of the chefs separated. """
    #Spearate the names of the chefs by ' e ' or ', '
    name = re.split(r' e |, ', name)
    if len(name) == 1:
        name = clean_chef_names(str(name[0]))
    else:
        name = [clean_chef_names(str(x)) for x in name]
    return name


def preprocess_chefs(index:int, chef_list:list):
    """Preprocesses the names of the chefs.
    Parameters:
        - index (int): Index of the chef in the list.
        - chef_list (list): List of chefs.
    Returns:
        - chef_list (str or list): Preprocessed name of the chef."""
    #If the chef_list is a list and the index is within the list length
    if isinstance(chef_list, list) and len(chef_list) > index:
        return chef_list[index]
    else:
        if index == 0:
            return chef_list
        else:
            return 'Not Applicable'
             

def standardize_location(location: str):
    """Standardizes a location string.
    Parameters:
        - location (str): Location of the restaurant.
    Returns:
        - location (str): Standardized location of 
        the restaurant."""

    
    #Handle different spellings of the same location
    location_mapping = {'alamansil': 'Almancil',
                        'lisbon': 'Lisboa', 'oporto':'Porto'}
    if location.lower() in location_mapping.keys():
        location = location_mapping[location.lower()]

    #Remove abbreviations
    location = re.sub(r's\.', 'São', location, flags=re.IGNORECASE)
    location = re.sub(r'sta\.', 'Santa', location, flags=re.IGNORECASE)
    location = re.sub(r'q\.ta', 'Quinta', location, flags=re.IGNORECASE)
    location = re.sub(r'M.nha', 'Marinha', location, flags=re.IGNORECASE)

    #Remove anything within brackets (inclusive):
    location = re.sub(r'\([^)]*\)', '', location)

    return standardize_text(location, keep_accents=True)


def generate_current_occupation(observation: dict):
    """Generates a random number of people currently at the restaurant 
    from a Normal Distribution.
    Parameters:
        - observation (dict): Restaurant information.
    Returns:
        - current_capacity (int): Number of people currently at the restaurant. """
    
    #If there is a maximum party size defined
    if np.isnan(observation['maxPartySize']) == False:
        max_party_size = observation['maxPartySize']
    #If it is nan
    else:
        max_party_size = 50

    #Check if the restaurant is open
    is_open = check_if_open(observation['schedule'])

    #If closed or not availbale set current capacity to 0
    if is_open == 'Closed':
        current_capacity = 0
    elif is_open == 'Not Available':
        current_capacity = 0
    #Otherwise generate a random number of people currently at the restaurant through a normal distribution
    else:
        party_size_distribution = np.random.normal(int(max_party_size/2), 
                                                   int(max_party_size/4), 100000)
        current_capacity = int(np.random.choice(party_size_distribution, 1))
    
    return current_capacity