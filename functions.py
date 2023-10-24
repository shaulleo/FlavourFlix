import numpy as np
import pandas as pd
#from currency_converter import CurrencyConverter
import datetime
import random


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
def check_if_open(restaurant_schedule, date=None):
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


# #Converts the average price of a restaurant to euros
# def to_euros(row):
#     """Converts the average price of a restaurant to euros.
#         Parameters:
#         - row (pandas.Series): Row of the dataframe.
#         Returns:
#         - euros (float): Average price of the restaurant in euros. """
#     c = CurrencyConverter()
#     if row['currency'] != 'EUR':
#         euros = c.convert(row['averagePrice'], row['currency'], 'EUR')
#     else:
#         euros = row['averagePrice']
#     return np.round(euros, 2)


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

        # Print the promotion schedules
        # for i, schedule in enumerate(promotion_schedules):
        #     print(f"Promotion {i+1}: {schedule['promotion_type']} at Restaurant {schedule['restaurant_id']} on {schedule['day_of_week']} from {schedule['start_time']} to {schedule['end_time']}")

        return promotion_schedules
    
    else:
        return 'No Offers'