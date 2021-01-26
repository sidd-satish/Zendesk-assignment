# Zendesk-assignment
This project is created using Python and Django. I have used Docker, with a Python image running on Ubuntu to make sure the project is working on the environment that is specified for the project.

## Part 1

Steps Followed:
Step 1 - I have created a parse.py file that creates a graph out of the CSV file that was given to me. This graph has a list of all possible previous and next stations that can be visited from a given station. This was done as part of the pre-processing and to convert the data to a format that will be easier to find the best routes from a certain source to destination station. This is stored in the static/ directory and the filename is data.json.

Step 2 - The server.py consists of the routes to the application. It internally calls other functions that are required in order to find the route from a source to destination station. 

The handle_data.py file consists of the helper functions required to manipulate the data and find the best route.

One thing to note is that -> When the source and destination stations are input, the program takes about 20 seconds to output the final route and it is not yet optimised to provide the best route quicker. Also no HTML overlay is added to show this, but can be seen on the browser. This is one of the assumptions I had made when writing the code.

Step 3 - The efficiency heuristic used to display the route is 'Shortest Route'. I have tried to find the shortest route (least number of stations) to visit for going from a certain source to destination. The code for this can be found in the handle_data.py file. There are 2 other functions that find any route and all possible routes from a certain source station to a destination station.

The assumption that I have made is that, I have assumed that even the stations that are to be opened in the future are already in the network. This is because the problem statement mentioned that this was a routing service for a future network. As a result, at certain times routes may be suggested that might involve going through stations or interchanges that are not currently functional.

Step 4 - The display of the routes is done in a list of lists format. This is to adhere to the requirement mentioned to display the route as - 'Routes should have one or more steps, like "Take [line] from [station] to [station]" or "Change to [line]"'.

A sample route is - 
[['Orchard', 'Dhoby Ghaut', {'NS'}], ['Dhoby Ghaut', 'Chinatown', {'NE'}], ['Chinatown', 'Jalan Besar', {'DT'}]]

This is ordered to fit the requirements. For finding the shortest route between Orchard and Jalan Besar, the route is as follows -

Take 'NS' line from Orchard to Dhoby Ghaut
Switch to 'NE' line
Take 'NE' line from Dhoby Ghaut to Chinatown
Switch to 'DT' line
Take 'DT' line from China Town to Jalan Besar

The API is running on port 5000 and /route is the route to a HTML form that takes input as source station and destination station. It can also be accessed through Postman and the POST request can be sent by sending the source and destination station under the variables - 'source_station' and 'dest_station'. These need to be sent using the form-data POST attributes.

Packaging of Code - 
All static files, including CSV and JSON files are stored in the static/ directory
All HTML code is stored in the templates/ directory
There is a Dockerfile in the root of the application
There is a requirements.txt file that consists of all packages being used in the project so that they can easily be installed

Steps to Run: (if you are using Docker)
1. Navigate to root of Project Dir
2. Run docker image build -t <image-name>:<tag> .
3. Run docker run -p 5001:5000 -d <image-name>:<tag>
4. Navigate to Localhost:5001/route on your system, after doing port-forwarding

If not using Docker
1. Navigate to root of Project Dir
2. pip install -r requirements.txt
3. python3 server.py
4. Navigate to localhost:5000/route

One of the assumptions that I have made here is that, since the problem statement mentioned API, I have not put much work into creating a UI that looks better. I have rather made it more functional. This fits with one of the requirements that is mentioned, which is 'Ease of use'

For testing - You can run python3 -m unittest test_handle_data.py.
There are unit test cases created for each of the helper function methods in handle_data.py.
Some of the functions internally call other functions. So I have not written unit test cases for those functions.

# Bonus

For the bonus part, my idea was to use a new graph that took into consideration - DT, CG and CE lines do not operate. So the graph created for Part 1 could be used for finding routes through the day and the new graph could be used for finding routes during night hours. I however, haven't yet been able to complete that piece of code and hence will not be committing that code along with this piece of code. I will commit it, once I have a working solution.

My idea was to use the shortest_route function and all_routes functions as in Part 1, which are modified to include the travel times between stations, as well as switches between lines. I thought this logic should have been sufficient in predicting the best route to take from a certain source station to a destination station, but I found that there was some bugs in my code. 