#!/bin/env python3
# This is a script to fetch train times and eventually display them on a mini LCD
# The API endpoint is <api.rtt.io> coming from <realtimetrains.co.uk>. All credits to swlines for this API

import os
import sys
import requests
import dotenv
import json
import argparse
from prettytable import PrettyTable

class Train: # Just to make the creation of trains a little neater
    def __init__(self, Headcode:str, Departure_station:str, Arrival_station:str, Booked_time:str, Real_time:str, OnTime:bool, Toc:str, Cancelled:bool=False) -> None:
        self.headcode = Headcode
        self.origStation = Departure_station
        self.terminus = Arrival_station
        self.booked_time = Booked_time
        self.real_time = Real_time
        self.onTime = OnTime
        self.toc = Toc
        self.cancelled = Cancelled


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
        cancelled = False # This needs to be reset each iteration

        if data['services'][i]['serviceType'] != "train":
            continue

        if data['services'][i]['locationDetail']['displayAs'] == "CANCELLED_CALL":
            cancelled = True

        # if data['services'][i]['trainIdentity']: # I think every train without being detailed has a train ID
        id = data['services'][i]['trainIdentity']

        origin = data['services'][i]['locationDetail']['origin'][0]['description']

        destination = data['services'][i]['locationDetail']['destination'][0]['description']
        
        # Now we get onto doing times 
        # If it begins at the station, then it's time should be when it departs, if it is calling then it's time is when it arrives, 
        # It isn't usually formatted that way but that is how I would like to do that, this is for larger stations, so you know when the train arrives and you can be there for it
        # If it is cancelled, check to see if there is an arrival time to see if it is meant to be a calling stop, if there isn't one then booked time is it's departure
        if data['services'][i]['locationDetail']['displayAs'] == "ORIGIN": 
            booked_time = data['services'][i]['locationDetail']['gbttBookedDeparture']

        elif data['services'][i]['locationDetail']['displayAs'] == "CALL":
            booked_time = data['services'][i]['locationDetail']['gbttBookedArrival']
        
        elif cancelled:
            if 'gbttBookedArrival' in data['services'][i]['locationDetail']:
                booked_time = data['services'][i]['locationDetail']['gbttBookedArrival']
            else:
                booked_time = data['services'][i]['locationDetail']['gbttBookedDeparture']
        else:
            booked_time = None

        # We also need it's real time, unless it is cancelled
        # First check if there is even a real time associated with the train, if not then the time is the same as booked time, we want the departure if it is origin, so check that first
        if cancelled:
            real_time = "N/A"

        elif data['services'][i]['locationDetail']['displayAs'] == "ORIGIN": # So it originates from this station
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
        if (real_time <= booked_time) and cancelled == False:
            on_time = True
        else:
            on_time = False
        
        # Grab the toc
        toc = data['services'][i]['atocName']

        train = Train(id, origin, destination, booked_time, real_time, on_time, toc, cancelled)

        trains.append(train)

    return(trains)


def get_times():
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

        return(request.text)

def parse_args(): # A function to read arguments, this will get expanded upon
    parser = argparse.ArgumentParser(prog="./main.py", description='Fetch train time information from "realtimetrains.com"')
    parser.add_argument('-k', '--keep', help='Dump the raw response into a file', action="store_true")
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

if args.keep:
    try:
        f = open("./rtt.json","w")
        f.write(raw_data)
        f.close()
    except:
        print("Failed to write file, skipping file writing")
try:
    json_data = json.loads(raw_data)

except:
    raise(json.JSONDecodeError)


trains = construct_trains(json_data) # Gets all of the trains needed

# Time for the table
table = PrettyTable()
table.field_names = ["Headcode", "TOC", "From", "Going to", "Booked time", "Expected"]

for train in trains:
    if (train.onTime == False) and train.cancelled == False:
        t = (train.real_time)
    
    elif train.cancelled == True:
        t = "Cancelled"

    else:
        t = "On time"

    table.add_row([train.headcode, train.toc, train.origStation, train.terminus, train.booked_time, t])

os.system("clear") # Clear the console before showing contents
print("Trains at " + json_data['services'][0]['locationDetail']['description'])
print(table)

if len(table.rows) > args.amount:
    print("One or more of the requested services are not trains and have been removed. The amount shown may not be the amount requested.")