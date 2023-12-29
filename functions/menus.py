import numpy as np
import pandas as pd
import datetime
import random
import re
from functions.env_colors import *
import ast
from deepl import Translator
from langdetect import detect
from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings
from functions.utils import *



def find_la_carte(json_body):
    """Slice the json body to find the "A la Carte" section.
    - Parameters:
       - json_body: json html body of the restaurant TheFork's page menu section.
    - Returns:
       - text: string containing the "A la Carte" section. """

    #Pattern to extract everything after the "A la Carte" string.
    pattern = r'div name=\\"A_LA_CARTE\\"(.*?)$'

    #Searching for matches
    match = re.search(pattern, json_body)

    if match:
        #If matches are found, extract everything after the target string
        text = match.group(1)
    else:
        text = None

    return text


def clean_section_name(json_body):
    """ Clean the section name.
    - Parameters:
       - json_body: json html body of the restaurant TheFork's page menu section.
       - Returns:
       - text: string containing the meal section name."""
    text = json_body.split("\\")
    text = text[3]
    text = text.replace('"', "")
    return text


def clean_menu_items(items):
    """Extract menu items and their information from a list of strings of html code 
    and return them formatted as a dictionary.
    - Parameters:
        - items: list of strings of html code.
    - Returns:
        - items_cleaned: dictionary containing menu items and their information in 
        the format: {meal_name: {isMainDish, price, description}}. """
    items_cleaned = {}

    for item in items:
        item = item.replace('\\"', '')
        item = item.replace('""', '"')
        item = item.replace('"{', '{')
        item = item.replace('}"', '}')
        pattern = r'([^,]+):([^,]+)'
        matches = re.findall(pattern, item)

        menu_item_dict = {key.strip(): value.strip() for key, value in matches}

        # Check if 'name' exists in menu_item_dict
        if 'name' in menu_item_dict:
            item_name = menu_item_dict['name']
        else:
            item_name = 'Unnamed Item'

        # Check if 'price' exists in menu_item_dict and can be converted to float
        price = None
        if 'price' in menu_item_dict:
            try:
                price = float(menu_item_dict['price'])
            except ValueError:
                pass

        # Check if 'isMainDish' exists in menu_item_dict
        is_main_dish = menu_item_dict.get('isMainDish', 'false').lower() == 'true'

        # Apply regex to 'description' to remove parentheses
        description = re.sub(r'[()]', '', menu_item_dict.get('description', '')).strip()

        item_dict = {
            item_name: {
                # 'isMainDish': is_main_dish,
                'price': price,
                'description': description
            }
        }
        items_cleaned.update(item_dict)

    return items_cleaned


def retrieve_menu(json_body):
    """ Retrieve the restaurant's menu from a JSON string containing the menu data.
    - Parameters:
        - json_body (str): JSON string containing the menu data.
    - Returns:
        - dict: Dictionary containing the menu data in the following format:
        {meal_section: {meal_name: {isMainDish, price, description}}}."""
    
    #Slice the initial json body to include everything after the "A LA CARTE" section.
    text = find_la_carte(json_body)
    
    #Split the text into meal sections.
    meals = text.split(':{\\"__typename\\":\\"RestaurantMenuSection\\')
    meals[-1] = meals[-1].split('{\\"__typename\\":\\"Opf\\"')[0]

    results = {}
    
    #For each meal section found
    for i in range(1, len(meals)):
        #Find the meals in the section
        section_meals = meals[i-1].split('{\\"__typename\\":\\"RestaurantMenuItem\\",')[1:-1]
        #Find the section name
        section_name = meals[i].split('{\\"__typename\\":\\"RestaurantMenuItem\\",')[0]
        #Clean the section name and the meals within the section
        section_name = clean_section_name(section_name)
        section_meals = clean_menu_items(section_meals)
        #Store in a dictionary the results
        results[section_name] = section_meals

    return results

