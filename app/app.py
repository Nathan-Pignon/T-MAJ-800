import os

penmon_path = os.path.abspath(os.path.dirname(__file__))
# Remove /api at the end
penmon_path = penmon_path[:-4]

import sys
sys.path.append(penmon_path)
sys.path.append(penmon_path + "/penmon")

from penmon.meteo_data_preparation import manage_meteorological_data
from penmon.meteo_data_visualization import generate_meteorological_data_visualization
from penmon.cities_data_preparation import get_cities_list, update_city_details, get_city_details

from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/")
def handle_index_view():
    return redirect("/penmon")


@app.route("/penmon", methods=['POST', 'GET'])
def handle_penmon_view():
    # Check if data/vineyards.csv exists
    vineyards = get_cities_list()

    if request.method == 'POST':
        data = request.json

        # Prepare data
        vineyard = data['vineyard']
        latitude = data['latitude']
        altitude = data['altitude']
        date = data['date']

        current_data = get_city_details(vineyard)
        if current_data["latitude"] != latitude or current_data["altitude"] != altitude:
            # Overwrite data
            manage_meteorological_data(vineyard, float(latitude), int(altitude), True)

            # Update vineyards.csv
            update_city_details(vineyard, latitude, altitude)

        else:
            # Generate meteorological data
            manage_meteorological_data(vineyard, float(latitude), int(altitude))

        # Generate data visualization
        result = generate_meteorological_data_visualization(vineyard, date)

        for key in result["month"]:
            result["month"][key].savefig(os.path.join(app.static_folder, f'month-{key}.png'))
            result["month"][key] = f'month-{key}.png'

        for key in result["year"]:
            result["year"][key].savefig(os.path.join(app.static_folder, f'year-{key}.png'))
            result["year"][key] = f'year-{key}.png'

        # Pass the figures array to the template
        return result
    return render_template('penmon.html', vineyards=vineyards)


@app.route("/penmon/vineyard/<name>", methods=['POST', 'GET'])
def handle_penmon_view_city(name: str):
    if request.method == 'POST':
        data = request.json
        return update_city_details(name, data['latitude'], data['altitude'])
    return get_city_details(name)
