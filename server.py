import flask
from flask import request, redirect, url_for, render_template
from datetime import date
from handle_data import findCode, createGraph, findRoute, allRoutes, shortestRoute, shortestTime, printRoute

if __name__ == '__main__':
    app = flask.Flask(__name__)

    # Test route to check if Flask in working
    @app.route('/')
    def hello_world():
        return render_template('index.html')

    # Route accepts arguments as form-data
    @app.route('/route', methods=["GET", "POST"])
    def route():
        if request.method == "POST":
            source_station = request.form.get('source_station')
            dest_station = request.form.get('dest_station')
            dest = findCode(dest_station)
            source = findCode(source_station)
            stations = createGraph('static/data.json')
            route = shortestRoute(stations, source, dest)
            routes = printRoute(route)
            return(str(routes))
        return render_template("views.html")

    # Route accepts arguments as form-data
    @app.route('/scheduler', methods=["GET", "POST"])
    def scheduler():
        if request.method == "POST":
            source_station = request.form.get('source_station')
            dest_station = request.form.get('dest_station')
            start_time = request.form.get('start_time')
            # Convert to required format to send to function
            time = start_time.split("T")
            dates = time[0].split("-")
            year = int(dates[0])
            month = int(dates[1])
            day = int(dates[2])
            dayOfWeek = date(year, month, day).isoweekday()
            hours = int(time[1][0:2])
            mins = int(time[1][-2:])
            dest = findCode(dest_station)
            source = findCode(source_station)
            # Use respective graph based on whether travel is during night or not
            if (hours >= 22 or hours < 6 or (hours == 6 and mins == 0)):
                stations = createGraph('static/bonus_data.json')
            else:
                stations = createGraph('static/data.json')
            timeTravelled = 0
            route = shortestTime(stations, source, dest, hours, mins, dayOfWeek, timeTravelled)
            # Travel during night time check
            if route == None:
                return("No available routes")
            else:
                routes = printRoute(route)
                return (str(routes))
        return render_template("display.html")

    app.run(debug=True, host='0.0.0.0')