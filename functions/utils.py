import numpy as np
import pandas as pd
import datetime
import re
import os
import unicodedata
import ast
from dotenv import find_dotenv, load_dotenv
import openai
from pydantic_settings import BaseSettings
from pydantic import Field, ValidationError, validate_call

# --------------------------------- 1. Load Environment Variables  --------------------------------

class Settings(BaseSettings):
    """ Loard Environment Variables """
    OPENAI_API_KEY: str = Field(validation_alias = "OPENAI_API_KEY")
    DATA_PATH: str = Field(validation_alias = "DATA_PATH")
    BING_MAPS_API_KEY: str = Field(validation_alias = "BING_MAPS_API_KEY")
    MAPS_BASE_URL: str = Field(validation_alias = "MAPS_BASE_URL")
    DETA_KEY: str = Field(validation_alias = "DETA_KEY")

_ = load_dotenv(find_dotenv())
if not _:
    _ = load_dotenv(".env")

local_settings = Settings()

# --------------------------------- 2. Utility Functions --------------------------------

#Standardizes user input when searching freely for a restaurant
def standardize_text(user_input_text: str, keep_accents: bool=False):
    """Standardizes a user input string for better matches.
    Parameters:
        - user_input_text (str): User input.
        - keep_accents (bool): If True, accents are not removed from the string.
    Returns:
        - user_input_text (str): Standardized user input.
    """
    if isinstance(user_input_text, str):
        #Convert to lower the string location
        user_input_text = user_input_text.lower()

        if not keep_accents:
            #Remove accents from the string
            user_input_text = unicodedata.normalize('NFKD', user_input_text).encode('ASCII', 'ignore').decode('utf-8')

        #Remove punctuation except numbers
        user_input_text = re.sub(r'[^\w\s]', ' ', user_input_text)

        #Remove single characters
        user_input_text = re.sub(r'\b\w\b', '', user_input_text)

        #remove multiple spaces
        user_input_text = re.sub(r'\s+', ' ', user_input_text)

        return user_input_text.strip()
    else:
        return None



#Checks if the restaurant is currently open
def check_if_open(restaurant_schedule:dict, date:str=None, time:str=None):
    """Checks if a given restaurant is open at the current time.
    Parameters:
        - restaurant_schedule (dict): Opening hours of the restaurant.
        - date (str): Date to check if the restaurant is open. If None, the current date is used.
    Returns:
        - open (str): 'Open' if the restaurant is open, 'Closed' otherwise.
    """
    #If no date is provided, use the current date
    if date is None:
        current_date = datetime.date.today()
    else:
        if type(date) == str:
            current_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        else:
            current_date = date

    #If no time is provided, use the current time
    if time is None:
        # Get the current time and format it accordingly.
        current_time = datetime.datetime.now().strftime("%H:%M")
        current_time = datetime.datetime.strptime(current_time, "%H:%M").time()
    else:
        if type(time) == str:
            current_time = datetime.datetime.strptime(time, '%H:%M').time()
        else:
            current_time = time

    day_of_week = current_date.strftime("%A")

    def check_schedule(schedule:str):
        """Checks if the restaurant is open at the current time.
        Parameters:
            - schedule (str): Schedule to check.
        Returns:
            - open (bool): True if the restaurant is open, False otherwise.
        """
        #Extract the opening and closing hours from the schedule
        opening_hours = schedule[:5]
        opening_hours = datetime.datetime.strptime(opening_hours, "%H:%M").time()
        closing_hours = schedule[-5:]
        #If the restaurant closes at midnight, change the closing time to 23:59
        if closing_hours == '24:00':
            closing_hours = '23:59'
        closing_hours = datetime.datetime.strptime(closing_hours, "%H:%M").time()
        #Check if the restaurant is open
        if  (opening_hours <= current_time) & (current_time <= closing_hours):
            return True
        else:
            return False

    if type(restaurant_schedule) == str:
        if restaurant_schedule == 'Not Available':
            return 'Not Available'
        else:
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





