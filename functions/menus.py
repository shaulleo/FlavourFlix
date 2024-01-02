import pandas as pd
from langdetect import *
from deep_translator import  GoogleTranslator
from functions import *
import re

def find_la_carte(json_body: str):
    """Slice the json body to find the "A la Carte" section.
    Parameters:
       - json_body (str): json html body of the restaurant TheFork's page menu section.
    Returns:
       - text (str): string containing the "A la Carte" section. """

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


def clean_section_name(json_body: str):
    """ Clean the section name.
    - Parameters:
       - json_body (str): json html body of the restaurant TheFork's page menu section.
       - Returns:
       - text (str): string containing the meal section name."""
    #Split the json body to extract the meal section name
    text = json_body.split("\\")
    #The meal section name is the fourth element of the list
    text = text[3]
    #Remove the quotation marks from the string
    text = text.replace('"', "")
    return text


def clean_menu_items(items: list[str]):
    """Extract menu items and their information from a list of strings of html code 
    and return them formatted as a dictionary.
    Parameters:
        - items (list[str]): list of strings of html code.
    Returns:
        - items_cleaned (dict): dictionary containing menu items and their information
         in the format: {meal_name: {isMainDish, price, description}}. 
    """
    #Create an empty dictionary
    items_cleaned = {}

    #For each item in the list
    for item in items:
        #Clean the string representing the item
        item = item.replace('\\"', '')
        pattern = r'([^,]+):([^,]+)'
        matches = re.findall(pattern, item)
        #Create a dictionary with the item information
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

        # Apply regex to 'description' to remove parentheses
        description = re.sub(r'[()]', '', menu_item_dict.get('description', '')).strip()

        item_dict = {
            item_name: {
                'price': price,
                'description': description
            }
        }
        items_cleaned.update(item_dict)

    return items_cleaned


def retrieve_menu(json_body: str):
    """ Retrieve the restaurant's menu from a JSON string containing the menu data.
    Parameters:
        - json_body (str): JSON string containing the menu data.
    Returns:
        - dict (dict): Dictionary containing the menu data in the following format:
        {meal_section: {meal_name: {isMainDish, price, description}}}."""
    
    #Slice the initial json body to include everything after the "A LA CARTE" section.
    text = find_la_carte(json_body)
    if text is None:
        return None
    
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


def extract_input(json_body:str):
    """Extract the input from the json body.
    Parameters:
        - json_body (str): json html body of the restaurant TheFork's page menu section.
    Returns:
        - extracted_value (str): string containing the input."""
    
    # Define the regular expression pattern
    pattern = r'"input": "(.*?)", "result"'

    # Use re.search to find the match
    match = re.search(pattern, json_body)

    # Check if a match is found
    if match:
        # Extract the value between "input" and "result"
        extracted_value = match.group(1)
        return str(extracted_value[:-5])
    else:
        return None
    

#Setting up two dictionaries which will store the translations to avoid calling the API unnecessarily
portuguese_to_eng = {}
eng_to_portuguese = {}

def translator_sentences(sentence:str, language:str, translator ):
    """Translate a sentence from Portuguese to English or vice-versa.
    Parameters:
        - sentence (str): string containing the sentence to be translated.
        - language (str): string containing the language to be translated.
        - translator (deep-translator Translator): Translator object instance.
    Returns:
        - translated_sentence (str): string containing the translated sentence."""
    
    #If the sentence is too short, don't translate
    if len(sentence) <= 3:
        translated_sentence = sentence

    try:
        #If the sentence is not in the target language and is not present in the dictionaries, translate it
        if (detect(sentence) != language) and (sentence not in portuguese_to_eng.keys() or sentence not in eng_to_portuguese.keys()):
            translated_sentence = translator.translate(sentence)
            #Store the translation in the corresponding dictionary
            if language == 'en':
                portuguese_to_eng[sentence] = translated_sentence
            else:
                eng_to_portuguese[translated_sentence] = sentence
        #If the sentence is in the dictionaries, retrieve its translation 
        elif sentence in portuguese_to_eng.keys() and language == 'en':
            translated_sentence = portuguese_to_eng[sentence]
        elif sentence in eng_to_portuguese.keys() and language == 'pt':
            translated_sentence = eng_to_portuguese[sentence]
        #If the sentence is in the target language, don't translate
        else:
            translated_sentence = sentence
        return translated_sentence
    #If there is an error, don't translate
    except Exception as e:
        print(f'Translation error: {e}')
        return translated_sentence
    

def translate_menus(menu:dict, language:str):
    """Translate the complete menu from Portuguese to English or vice-versa.
    Parameters:
        - menu (dict): dictionary containing the menu.
        - language (str): string containing the language to be translated.
    Returns:
        - translated_menu (dict): dictionary containing the translated menu.
    """
    #Set up the translator object, if the target language is not supported, return None
    if language=='en' or language=='pt':
        translator = GoogleTranslator(source='auto', target=language)
    else:
        return None
    try:
        #For each section in the menu, translate the section name and the items
        translated_menu = {}
        for section in menu.keys():
            translated_section = translator_sentences(section, language, translator)
            #Store the translated sections in a dictionary
            section_dict = {}
            #For each item in the section, translate the name and the description if it exists
            for item in menu[section].keys():
                translated_food = translator_sentences(item, language, translator)
                description = menu[section][item]['description']
                if description != 'null':
                    translated_description = translator_sentences(description, language, translator)
                else:
                    translated_description = description
                #Store the translated items in a dictionary with their respective prices and translated descriptions
                item_dict = {'price': menu[section][item]['price'], 'description': translated_description}
                #Finalize the menu dictionary
                section_dict[translated_food] = item_dict
            translated_menu[translated_section] = section_dict
        return translated_menu
    except Exception as e:
        print(f'Translation error: {e}')
        return None