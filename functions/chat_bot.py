
"""
ChatBot class
"""

import random


# [i] Static ChatBot                                                                               -

class ChatBotStatic:
    """
    ChatBot class
    """

    def __init__(self):
        self.memory = []

    def generate_response(self, message: str):
        """
        Returns a static response
        """
        return "How can I help you?"


# [i] Static ChatBot                                                                               -

class ChatBotRandom:
    """
    ChatBotRandom class provides a simple chatbot that generates random responses.
    """

    def __init__(self):
        self.memory = []

    def generate_response(self, message: str):
        """
        Generates a random response for incoming messages.

        Returns:
            str: A randomly selected response from a list of greeting messages.

        """
        return random.choice(
            [
                "Hello there! How can I assist you today?",
                "Hi, human! Is there anything I can help you with?",
                "Do you need help?",
            ]
        )


class ChatBot:
    """
    Generate a response by using LLMs.
    """

    def __init__(self):
        self.memory = []

    def generate_response(self, message: str):
        """
        Generate a response by using LLMs.
        """
        return self.model.get_completion(message)
    

    
class ChatBot:
    """
    Generate a response by using LLMs.
    """
    def __init__(self, model_manager):
        self.memory = []
        #my_GPT = GPTWrapper(local_settings.OPENAI_API_KEY)
        self.model = model_manager

    def generate_response(self, message: str):
        """
        Generate a response by using LLMs.
        """
        return self.model.get_completion(message)