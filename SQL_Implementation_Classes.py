import sqlite3
import random

class FlightAndPassengerInformation:

    # Get The Passenger Information via User Input
    
    def __init__(self):
        self.flightNumber = input("Enter Flight Number: ")
        self.customerFirstName = input("Enter Passenger First Name: ")
        self.customerLastName = input("Enter Passenger Last Name: ")
        self.flightDate = input("Enter flight date YYYY-MM-DD: ")
    
        self.delayURL =  "https://aerodatabox.p.rapidapi.com/flights/number/" + self.flightNumber + "/" + self.flightDate

        print(self.delayURL)
        self.headers = {
            'x-rapidapi-key': " ",
            'x-rapidapi-host': "aerodatabox.p.rapidapi.com"
           }
        self.request = requests.request("GET", self.delayURL, headers=self.headers)
        self.response = self.request.text
        
class Database(object):
    
    # sqlite3 database class that holds testers jobs.
    
    DB_LOCATION = "wallet.sqlite"

    def __init__(self, db_location=None):
        """Initialize db class variables"""
        if db_location is not None:
            self.connection = sqlite3.connect(db_location)
        else:
            self.connection = sqlite3.connect(self.DB_LOCATION)
        self.cur = self.connection.cursor()