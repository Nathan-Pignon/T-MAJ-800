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

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/penmon", methods=['POST', 'GET'])
def handle_penmon_view():
    # Check if data/cities.csv exists
    cities = get_cities_list()

    if request.method == 'POST':
        data = request.json

        # Prepare data
        city = data['city']
        latitude = data['latitude']
        altitude = data['altitude']

        current_data = get_city_details(city)
        if current_data["latitude"] != latitude or current_data["altitude"] != altitude:
            # Overwrite data
            manage_meteorological_data(city, float(latitude), int(altitude), True)

            # Update cities.csv
            update_city_details(city, latitude, altitude)

        else:
            # Generate meteorological data
            manage_meteorological_data(city, float(latitude), int(altitude))

        # Generate data visualization
        figures = generate_meteorological_data_visualization(city)

        # Save each figure as an image file
        response = []
        for i, fig in enumerate(figures):
            fig.savefig(os.path.join(app.static_folder, f'figure{i + 1}.png'))
            response.append(f'figure{i + 1}.png')

        # Pass the figures array to the template
        return {
            'figures': response
        }
    return render_template('penmon.html', cities=cities)


@app.route("/penmon/city/<name>", methods=['POST', 'GET'])
def handle_penmon_view_city(name: str):
    if request.method == 'POST':
        data = request.json
        return update_city_details(name, data['latitude'], data['altitude'])
    return get_city_details(name)
