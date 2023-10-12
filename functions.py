import numpy as np
import pandas as pd
from currency_converter import CurrencyConverter
import datetime


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


