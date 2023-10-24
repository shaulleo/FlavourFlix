import numpy as np
import pandas as pd
#from currency_converter import CurrencyConverter
import datetime
import random
import re
import unicodedata
import ast

# ------------------------------- General Functions --------------------------------


# ------------------------------- 1. Original Data Preprocessement --------------------------------

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

        schedule_time = schedule[day_of_week]
        schedule_times = schedule_time.split(',')
        if len(schedule_times) > 1:
            first_period = schedule_times[0]
            f_period_open = first_period[:5]
            f_period_close = first_period[-5:]

            second_period = schedule_times[-1]
            s_period_open = second_period[:5]
            s_period_close = second_period[-5:]
        else:
            whole_day = schedule_times[0]
            w_day_open = whole_day[:5]
            w_day_close = whole_day[-5:]


        # Define the promotion schedule
        if promotion_type == 'Happy Hour':
            if second_period:
                start_time = f"{random.randint(2, 4)}:{random.choice(['00', '15', '30', '45'])}pm"
                end_time = f"{random.randint(5, 7)}:{random.choice(['00', '15', '30', '45'])}pm"
            elif first_period:
                start_time = f"{random.randint(2, 4)}:{random.choice(['00', '15', '30', '45'])}pm"
                end_time = f"{random.randint(5, 7)}:{random.choice(['00', '15', '30', '45'])}pm"
            else:
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


# --------------------------------- 2. Utility Functions --------------------------------

#Standardizes user input when searching freely for a restaurant
def standardize_text(user_input_text):
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



#Checks if the restaurant is currently open
def check_if_open(restaurant_schedule, date=None, time=None):

    """Checks if a given restaurant is open at the current time.
        Parameters:
        - restaurant_schedule (dict): Opening hours of the restaurant.
        - date (str): Date to check if the restaurant is open. If None, the current date is used.
        Returns:
        - open (str): 'Open' if the restaurant is open, 'Closed' otherwise. """
    

    if date is None:
        current_date = datetime.date.today()
    else:
        current_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

    if time is None:
        # Get the current time and format it accordingly.
        current_time = datetime.datetime.now().strftime("%H:%M")
        current_time = datetime.datetime.strptime(current_time, "%H:%M").time()
    else:
        current_time = datetime.datetime.strptime(time, '%H:%M').time()

    day_of_week = current_date.strftime("%A")

    def check_schedule(schedule):
        opening_hours = schedule[:5]
        opening_hours = datetime.datetime.strptime(opening_hours, "%H:%M").time()
        closing_hours = schedule[-5:]
        if closing_hours == '24:00':
            closing_hours = '23:59'
        closing_hours = datetime.datetime.strptime(closing_hours, "%H:%M").time()
        if  (opening_hours <= current_time) & (current_time <= closing_hours):
            return True
        else:
            return False


    if type(restaurant_schedule) == str:
        restaurant_schedule = ast.literal_eval(restaurant_schedule)
    elif type(restaurant_schedule) == dict:
        pass
    else: 
        return 'Not Available'
    

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

