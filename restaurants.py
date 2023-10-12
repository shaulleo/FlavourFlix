class Restaurant:
    def __init__(self, name, cuisine, price, ratingsummary,address, phone, website, schedule, menu, reviews, style, latitude, longitude,  city, photo, averageprice):
        self.name = name
        self.cuisine = cuisine
        self.price = price
        self.ratingsummary = ratingsummary
        self.address = address
        self.phone = phone
        self.website = website
        self.schedule = schedule
        self.menu = menu
        self.reviews = reviews
        self.style = style
        self.latitude = latitude
        self.longitude = longitude
        self.city = city
        self.photo = photo
        self.menu = None

    def get_menu():
        pass

    def check_if_open():
        pass

    def reserve():
        pass

    def get_info():
        pass

    def __str__():
        pass


class Menu:
    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description
