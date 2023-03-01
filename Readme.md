# A program to fetch and prettify train times from [Realtime trains](https://realtimetrains.com/)  
This is a program that does what it says on the tin, using the [Realtime Trains API](https://api.rtt.io/) to collect and nicely display train times for a given station. Thanks to the devs at Realtime Trains for this public API, this would not be possible without it.  
This is for another project which I'm working on whereby I have a little lcd on my desk and can use a raspberry PI to display train times. But that is out of the scope for this project.  
As with anything I do, I couldn't find something that did what I wanted so I made it myself. My programming skills are passable but they get the job done.  
## Pre-Requisites:  
For this program you will need:  
- An account over at [Realtime Trains](https://realtimetrains.com/) (more on that in a later section)  
- Python 3 (made using Python 3.8.10)  
- python-dotenv - https://github.com/theskumar/python-dotenv/
- prettytable - https://github.com/jazzband/prettytable  
- Git
- Not necessary but this was made on linux and that is what it is designed to run on. I won't be providing windows support if there are any issues
  
## Getting started:  
1. First, you need an account with the Realtime Trains API, owned by [Tom Cairns](https://twitter.com/swlines). Head to https://apit.rtt.io/ and create an account
2. Next, open a terminal and run "git clone https://git.birb.not.hpkns.uk/hbirb/rtt_fetcher && cd rtt_fetcher"
3. Change the name of ".env.example" to ".env"
4. Open the now ".env" file and in the "UNAME" and "PASSWORD" fields, enter your **API credentials**, not your account credentials. These are provided on the API dashboard
5. Next, enter the CRS code for the default station you want to search for. (If you are unsure, look [here](http://www.railwaycodes.org.uk/crs/crs0.shtm))
6. Follow usage steps  
  
## Usage:  
usage: ./main.py [-h] [-s BHM] [-a 5]  
  
Fetch train time information from "realtimetrains.com"  
  
optional arguments:  
&emsp;-h, --help&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;show this help message and exit  
&emsp;-s BHM, --station BHM&emsp;&emsp;Passing a station's CRS code through argument instead of in the .env file                    
&emsp;-a 5, --amount 5&emsp;&emsp;&emsp;&emsp;&emsp;The amount of services to print out, default 5  
## Examples:  
