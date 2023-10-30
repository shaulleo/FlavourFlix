import pandas as pd 
import numpy as np
import random
import string


class UserLogin:
    def __init__(self, email=None, username=None):
        self.email = email
        self.username = username
        self.logged_on = False
        self.entry_code = None

    # def login(self):
    #     #self.entry_code = self.generate_code()
    #     #self.send_code(self.entry_code)
    #     #user_code = self.request_code()
    #     while user_code != self.entry_code:
    #         print('Ups! It seems that your code is incorrect. Please try again.')
    #         user_code = self.request_code()
    #     self.logged_on = True

    def is_registered(self, userdatabase):
        if ((self.email in userdatabase['email'].values) or (self.username in userdatabase['username'].values)):
            return True
        else:
            return False
        
    def generate_code(self):
        if (self.logged_on == False) and (self.email is not None):
            characters = string.ascii_uppercase + string.digits
            code = ''.join(random.choice(characters) for _ in range(5))
            self.entry_code = code

    def send_code(self, code):
        # Your email sending code can go here
        print(f'Your code is: {code}')

    def request_code(self):
        user_code = input('Please enter your code:\n')
        while user_code != self.entry_code:
            print('Ups! It seems that your code is incorrect. Please try again.')
            user_code = self.request_code()
        self.logged_on = True