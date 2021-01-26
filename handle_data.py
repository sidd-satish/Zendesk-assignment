import csv
import json

minTime = float('inf')

# Convert Input from form to station code
def findCode(station):
    with open('static/StationMap.csv') as sm:
        reader = csv.reader(sm, delimiter=",", quotechar='"')
        data_read = [row for row in reader]
    # Dictionary with key as station name and value as all possible station codes
    res = {}
    for i in range(1, len(data_read)):
        if data_read[i][1] in res:
            temp = res[data_read[i][1]] + "/" + data_read[i][0]
            res[data_read[i][1]] = temp
        else:
            res[data_read[i][1]] = data_read[i][0]
    return res[station]

# Convert Station code to Station name
def findStation(code):
    with open('static/StationMap.csv') as sm:
        reader = csv.reader(sm, delimiter=",", quotechar='"')
        data_read = [row for row in reader]
    # Dictionary with key as station name and value as all possible station codes
    res = {}
    for i in range(1, len(data_read)):
        if data_read[i][1] in res:
            temp = res[data_read[i][1]] + "/" + data_read[i][0]
            res[data_read[i][1]] = temp
        else:
            res[data_read[i][1]] = data_read[i][0]
    for station, scode in res.items():
        if scode == code:
            return(station)

# Load graph (data.json) -> Created by running parse.py (Part of Pre-processing)
def createGraph(file):
    with open(file) as f:
        data = json.load(f)
        return data

# First route from graph (Irrespective of time, hops, etc)
def findRoute(graph, source, dest, route=[]):
    route = route + [source]
    if source == dest:
        return route
    if source not in list(graph.keys()):
        return None
    for node in graph[source]:
        if node not in route:
            newRoute = findRoute(graph, node, dest, route)
            if newRoute:
                return newRoute
    return None

# Find all routes
def allRoutes(graph, source, dest, route=[]):
    route = route + [source]
    if source == dest:
        return [route]
    if source not in list(graph.keys()):
        return []
    routes = []
    for node in graph[source]:
        if node not in route:
            newRoutes = allRoutes(graph, node, dest, route)
            for newRoute in newRoutes:
                routes.append(newRoute)
    return routes

# Find shortest route
def shortestRoute(graph, source, dest, route=[]):
    route = route + [source]
    if source == dest:
        return route
    if source not in list(graph.keys()):
        return None
    shortest = None
    for node in graph[source]:
        if node not in route:
            new_route = shortestRoute(graph, node, dest, route)
            if new_route:
                if not shortest or len(new_route) < len(shortest):
                    shortest = new_route
    return shortest

# Find shortest route with traffic
def shortestTime(graph, source, dest, hours, mins, dayOfWeek, timeTravelled, route=[]):
    global minTime
    sourceList = source.split("/")
    switchLine = 0
    # Set flag for when a switch is made
    if len(route) > 1:
        fList = route[len(route)-1].split("/")
        sList = route[len(route)-2].split("/")
        sourceList = source.split("/")
        cLine = set(fList).intersection(sList)
        dLine = set(fList).intersection(sourceList)
        if cLine != dLine:
            switchLine = 1
        else:
            switchLine = 0
    # Peak Hours Case
    if ((hours >= 6 or hours < 9 or (hours == 9 and mins == 0)) or (hours >= 18 or hours < 21 or (hours == 21 and mins == 0))) and (dayOfWeek < 6):
        if 'NS' in source or 'NE' in source:
            timeTravelled += 12
        else:
            timeTravelled += 10
        # Make Switch?
        if switchLine == 1:
            timeTravelled += 15
    # Night Hours Case
    elif (hours >= 22 or hours < 6 or (hours == 6 and mins == 0)):
        if 'TE' in source:
            timeTravelled += 8
        else:
            timeTravelled += 10
        # Make Switch?
        if switchLine == 1:
            timeTravelled += 10
    # Non-peak hours Case
    else:
        if 'DT' in source or 'TE' in source:
            timeTravelled += 8
        else:
            timeTravelled += 10
        # Make Switch?
        if switchLine == 1:
            timeTravelled += 15
    route = route + [source]
    if source == dest:
        return route
    if source not in list(graph.keys()):
        return None
    shortest = None
    for node in graph[source]:
        if node not in route:
            new_route = shortestTime(graph, node, dest, hours, mins, dayOfWeek, timeTravelled, route)
            if new_route:
                # Assign new route if travel time is lesser
                if not shortest or (len(new_route) < len(shortest) and timeTravelled < minTime):
                    minTime = timeTravelled
                    shortest = new_route
    return shortest

# Convert route to format required
def printRoute(route):
    routes = []
    r = []
    firstVal = 0
    secVal = 1
    firstValList = route[firstVal].split("/")
    firstValList = [x[0:2] for x in firstValList]
    secValList = route[secVal].split("/")
    secValList = [x[0:2] for x in secValList]
    # Find common line between two stations
    mainLine = set(firstValList).intersection(secValList)
    while firstVal <= secVal and secVal < len(route):
        firstValList = route[firstVal].split("/")
        firstValList = [x[0:2] for x in firstValList]
        secValList = route[secVal].split("/")
        secValList = [x[0:2] for x in secValList]
        line = set(firstValList).intersection(secValList)
        if len(r) == 0:
            r.append(findStation(route[firstVal]))
        # Continue using same line if two stations have a line in common
        if mainLine == line:
            firstVal += 1
            secVal += 1
        # Make switch to new line and add previous source, dest and line to list
        else:
            sStation = findStation(route[firstVal])
            r.append(sStation)
            dStation = findStation(route[secVal])
            r.append(mainLine)
            routes.append(r)
            r = []
            r.append(sStation)
            firstVal = secVal
            secVal += 1
            mainLine = line
    r.append(findStation(route[len(route)-1]))
    r.append(mainLine)
    routes.append(r)
    # Handling case where both source and dest are on same line
    if len(routes) == 0:
        r = []
        sStation = findStation(route[0])
        r.append(sStation)
        dStation = findStation(route[len(route)-1])
        r.append(dStation)
        r.append(mainLine)
        routes.append(r)
    return(routes)

# # Test Input
# dest = findCode('Esplanade')
# source = findCode('Bugis')
# print(source)
# stations = createGraph('data.json')

# # Find first route
# route2 = findRoute(stations, source, dest)
# print(route2)
# # Find all routes
# route1 = allRoutes(stations, source, dest)
# print(len(route1))
# Find shortest route
# route = shortestRoute(stations, source, dest)
# routes = printRoute(route)
# print(route)
# print(routes)