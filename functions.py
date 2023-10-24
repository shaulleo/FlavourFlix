import numpy as np
import pandas as pd
#from currency_converter import CurrencyConverter
import datetime
import random
import re
import unicodedata

# ------------------------------- General Functions --------------------------------

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


#Checks if the restaurant is currently open
def check_if_open(restaurant_schedule, date=None, time=None):
    #Ajustar consoante horas também

    """Checks if a given restaurant is open at the current time.
        Parameters:
        - restaurant_schedule (dict): Opening hours of the restaurant.
        - date (str): Date to check if the restaurant is open. If None, the current date is used.
        Returns:
        - open (str): 'Open' if the restaurant is open, 'Closed' otherwise. """
    
    #Confirmar se está a funcionar 100%
    if date is None:
        current_date = datetime.date.today()
    else:
        current_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

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

    if restaurant_schedule == 'Not Available':
        return 'Not Available'
    elif restaurant_schedule[day_of_week] == 'Closed':
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


def promotion_generator(schedule, num_promotions, prob):
    #ajustar consoante horas
    """Generates a promotion schedule for a restaurant.
        Parameters:
        - schedule (dict): Restaurant Schedule.
        - num_promotions (int): Maximum number of promotions to generate per restaurant.
        - prob (float): Probability of a restaurant having promotions.
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
        # Create a list of promotion schedules
        promotion_schedules = []

        # Loop over each promotion
        i = 0
        while i < num_promotions:
            # Choose a random day of the week

            day_of_week = random.choice(days_of_week)
            # Choose a random promotion type
            promotion_type = random.choice(promotion_types)

            # Choose a random start time and end time based on promotion type
            if promotion_type == 'Happy Hour':
                start_time = f"{random.randint(2, 4)}:{random.choice(['00', '15', '30', '45'])}pm"
                end_time = f"{random.randint(5, 7)}:{random.choice(['00', '15', '30', '45'])}pm"
            elif promotion_type == '20% off':
                start_time = f"{random.randint(6, 8)}:{random.choice(['00', '15', '30', '45'])}pm"
                end_time = f"{random.randint(9, 11)}:{random.choice(['00', '15', '30', '45'])}pm"
            elif promotion_type == 'None':
                start_time = 'None'
                end_time = 'None'
            else:
                start_time = f"{random.randint(5, 7)}:{random.choice(['00', '15', '30', '45'])}pm"
                end_time = f"{random.randint(8, 10)}:{random.choice(['00', '15', '30', '45'])}pm"

            # Add the promotion schedule to the list
            promotion_schedules.append({
                'promotion_type': promotion_type,
                'day_of_week': day_of_week,
                'start_time': start_time,
                'end_time': end_time,
            })

            i += 1
            if random.random() < 0.2:
                i = num_promotions

        return promotion_schedules
    
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

    return standardize_filters(location)

def standardize_filters(user_input_text):
    """Standardizes a user input string for better matches.
        Parameters:
        - user_input_text (str): User input.
        Returns:
        - user_input_text (str): Standardized user input."""

    #Convert to lower the string location
    user_input_text = user_input_text.lower()

    #Remove accents from the string
    user_input_text = unicodedata.normalize('NFKD', user_input_text).encode('ASCII', 'ignore').decode('utf-8')

    #Remove ponctuation except numbers
    user_input_text = re.sub(r'[^\w\s]', ' ', user_input_text)

    #Remove single characters
    user_input_text = re.sub(r'\b\w\b', '', user_input_text)

    #remove multiple spaces
    user_input_text = re.sub(r'\s+', ' ', user_input_text)

    return user_input_text.strip()
