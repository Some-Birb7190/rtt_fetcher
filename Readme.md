<h1>Hello, this is a small project I am working by myself</h1>

For anyone that wants to use this program, you must have these following libraries installed.<br />
&emsp;- dotenv<br />
&emsp;- argparse<br />
&emsp;- requests<br />
&emsp;- json<br />
And any other that are mentioned in the `import` statements at the top of `main.py`. <br />
<br />

<h2>For authentication features:</h2>
&emsp;1- You must create an API account over at https://api.rtt.io/.<br />
&emsp;2- Navigate to the file `.env.example`<br />
&emsp;3- Place your username and password **that the api gives you, not your account UN/PW!** <br />
&emsp;4- Remove the `.example` on the end of the file, so it should just be `.env` <br />
<br />

<h2>Passing arguments:</h2>
To view the arguments that this program can take, run `./main.py -h` and it will print it out. Alternatively it is printed here.<br />
All of these arguments are optional and the program will run just fine without them:<br />
&emsp;-h, --help&emsp;&emsp;Show the help message<br />
&emsp;-f &emsp;&emsp;&emsp;&emsp;&emsp;Specify a file location to use (preferrably files with no spaces)<br />
&emsp;-c &emsp;&emsp;&emsp;&emsp;&emsp;Force the program to use the file cache<br />
&emsp;-d &emsp;&emsp;&emsp;&emsp;&emsp;Force the program to fetch a new dump<br />
&emsp;-s &emsp;&emsp;&emsp;&emsp;&emsp;Passing a station code through arguments instead of typing it in<br />
&emsp;-a &emsp;&emsp;&emsp;&emsp;&emsp;The amount of services to print out, rather than just parsing the entire dump/file<br />

