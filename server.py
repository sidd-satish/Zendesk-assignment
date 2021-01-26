import flask
from flask import request, redirect, url_for, render_template
from handle_data import findCode, createGraph, findRoute, allRoutes, shortestRoute, printRoute

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

    app.run(debug=True, host='0.0.0.0')