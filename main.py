#!/bin/env python3
# This is a script to fetch train times and eventually display them on a mini LCD
# The API endpoint is <api.rtt.io> coming from <realtimetrains.co.uk>. All credits to swlines for this API

import os
import sys
import requests
import dotenv
import json
import time
import argparse
from prettytable import PrettyTable

class Train: # Just to make the creation of trains a little neater
    def __init__(self, Headcode:str, Departure_station:str, Arrival_station:str, Booked_time:str, Real_time:str, OnTime:bool, Toc:str) -> None:
        self.headcode = Headcode
        self.origStation = Departure_station
        self.terminus = Arrival_station
        self.booked_time = Booked_time
        self.real_time = Real_time
        self.onTime = OnTime
        self.toc = Toc


def construct_trains(data):
    if data['services'] == None: # Check if there are trains
        print("There are no trains at this station!")
        sys.exit(1)
    
    else:
        if args.amount > len(data['services']):
            count = len(data['services'])
        else:
            count = args.amount
        
    trains = [] # The array that will hold all of the train objects
    for i in range(0,count):
        if data['services'][i]['serviceType'] != "train":
            print("One or some of these services are not trains, the amount displayed may not be the actual amount requested")
            continue

        if data['services'][i]['trainIdentity']:
            id = data['services'][i]['trainIdentity']
        else:
            id = None

        if data['services'][i]['locationDetail']['origin']:
            origin = data['services'][i]['locationDetail']['origin'][0]['description']
        else:
            origin = None

        if data['services'][i]['locationDetail']['destination']:
            destination = data['services'][i]['locationDetail']['destination'][0]['description']
        else:
            destination = None
        
        #Now we get onto doing times 
        #If it begins at the station, then it's time should be when it departs, if it is stopping then it's time is when it arrives
        if data['services'][i]['locationDetail']['displayAs'] == "ORIGIN": 
            booked_time = data['services'][i]['locationDetail']['gbttBookedDeparture']

        else:
            booked_time = data['services'][i]['locationDetail']['gbttBookedArrival']
        
        # We also need it's real time
        # First check if there is even a real time associated with the train, if not then the time is the same as booked time, we want the departure if it is origin, so check that first
        if data['services'][i]['locationDetail']['displayAs'] == "ORIGIN": # So it originates from this station
            if data['services'][i]['locationDetail']['realtimeDeparture']: # Does it have a departure
                real_time = data['services'][i]['locationDetail']['realtimeDeparture']
            else:
                real_time = booked_time
        else: # No it passes through, so do the same but with arrival
            if data['services'][i]['locationDetail']['realtimeArrival']:
                real_time = data['services'][i]['locationDetail']['realtimeArrival']
            else:
                real_time = booked_time
        
        # So we have the real and booked time, check if it is on time
        if (real_time <= booked_time):
            on_time = True
        else:
            on_time = False
        
        # Grab the toc
        toc = data['services'][i]['atocName']

        train = Train(id, origin, destination, booked_time, real_time, on_time, toc)

        trains.append(train)

    return(trains)


def get_times() -> dict:
    URL = "https://api.rtt.io/api/v1/json/search/" + STATION # This location will not get arrivals, so terminating trains will not show up, however starting ones will
    
    request = requests.get(URL, auth=(USERNAME,PASSWORD))

    if request.status_code == 404:
        print("The requested station could not be found.")
        sys.exit(1)
    
    elif request.text == "{\"error\":\"unknown error occurred\"}":
        print("An unknown server error ocurred.")
        sys.exit(1)
    
    elif request.status_code == 401:
        print("Authentication required/incorrect.")

    elif (int(request.status_code/100)) == 2: # Check if the response code begins with 2

        try:
            t = json.loads(request.text)
            return(t)

        except(json.JSONDecodeError):
            print("Failed to decode JSON body")
        

def parse_args(): # A function to read arguments, this will get expanded upon
    parser = argparse.ArgumentParser(prog="./main.py", description='Fetch train time information from "realtimetrains.com"')
    # parser.add_argument('-f', metavar='./rtt.json', help='Specify a file location to use (preferrably files with no spaces).')
    # parser.add_argument('-c', help='Force program to use cache', action="store_true")
    # parser.add_argument('-d', help='Force program to fetch new dump', action="store_true")
    #parser.add_argument('-r', help='When program reaches the end, allow the program to refresh every five minutes with new information.', action="store_true")
    parser.add_argument('-s', '--station', help='Passing a station\'s CRS code through argument instead of in the .env file', metavar='BHM' )
    parser.add_argument('-a', '--amount', help='The amount of services to print out, default 5', metavar='5', default=5, type=int)
    return(parser.parse_args())

# End of function definitions

# Grab any arguments
args = parse_args()

# Get .env variables
dotenv.load_dotenv(dotenv.find_dotenv())
USERNAME = os.environ["UNAME"]
PASSWORD = os.environ["PASSWORD"]
STATION = os.environ["STATION"].upper()

if args.station:
    STATION = (args.station).upper()

# Grab the list of times and try to parse it
raw_data = get_times()
trains = construct_trains(raw_data) # Gets all of the trains needed

# Time for the table
table = PrettyTable()
table.field_names = ["Headcode", "TOC", "From", "Going to", "Booked time", "Real time"]

for train in trains:
    if train.onTime == False:
        t = ("Exp: " + train.real_time)
    else:
        t = "On time"
    table.add_row([train.headcode, train.toc, train.origStation, train.terminus, train.booked_time, t, ])

print("Trains at " + raw_data['services'][0]['locationDetail']['description'])
print(table)