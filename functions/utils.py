import numpy as np
import pandas as pd
import datetime
import re
import unicodedata
import ast
from functions.preprocessement import *
from functions.env_colors import *
from functions.location import *



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

