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
1. First, you need an account with the Realtime Trains API, owned by [Tom Cairns](https://twitter.com/swlines). Head to https://api.rtt.io/ and create an account
2. Next, open a terminal and run `git clone https://github.com/some-birb7190/rtt_fetcher.git && cd rtt_fetcher`
3. Change the name of ".env.example" to ".env"
4. Open the now ".env" file and in the "UNAME" and "PASSWORD" fields, enter your **API credentials**, not your account credentials. These are provided on the API dashboard
5. Next, enter the CRS code for the default station you want to search for into the "STATION" field. (If you are unsure, look [here](http://www.railwaycodes.org.uk/crs/crs0.shtm))  
6. If you are on Linux, open a terminal in the folder of "./main.py" and run "chmod +x ./main.py" so you can execute it  
7. Follow usage steps  
  
## Usage:  
usage: `./main.py [-h] [-k] [-s BHM] [-a 5]`  
  
Fetch train time information from "realtimetrains.com"  
  
<!-- options:  
&emsp;-h, --help&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;show this help message and exit  
&emsp;-k, --keep &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;Dump the raw JSON into a file (rtt.json)   
&emsp;-s BHM, --station BHM&emsp;&emsp;Passing a station's CRS code through argument instead of in the .env file                    
&emsp;-a 5, --amount 5&emsp;&emsp;&emsp;&emsp;&emsp;The amount of services to print out, default 5  
-->

| Option                | Action                                                                   |
|-----------------------|--------------------------------------------------------------------------|
| -h, --help            | show this help message and exit                                          |
| -k, --keep            | Dump the raw response into a JSON file (rtt.json)                        |
| -s BHM, --station BHM | Pass a station's CRS code through this argument instead of the .env file |
| -a 5, --amount 5      | The amount of services to print out, default 5                           |  
  
## Examples:  
Output the help statement(`./main.py -h`):  
![Output the help statement gif](readme-content/help_example.gif)  
    
Output the next 5 (the default amount) for the default station in ".env" (`./main.py`):  
![Output default parameter](readme-content/example_output.gif)  

Output the next 10 trains at a different station (`./main.py --amount 10 --station HHD`):  
![Custom output with arguments](readme-content/argument_example.gif)  
## Final notes:  
Again a huge thanks to the team at Realtime Trains as this wouldn't be possible without them.  
Yes this code is awful but I wanted to make it work and I think I did that pretty well.  
  
If you have any issues you would like to submit, please ensure that the problem relates to the code itself (EG malfunction or something failing) rather than a system specific one (EG it doesn't run on Windows whatever).
