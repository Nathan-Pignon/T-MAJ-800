import os
penmon_path = os.path.abspath(os.path.dirname(__file__))
# Remove /api at the end
penmon_path = penmon_path[:-4]

import sys
sys.path.append(penmon_path)
sys.path.append(penmon_path + "/penmon")

from penmon.data_preparation import prepare_data
from penmon.data_visualization import generate_data_visualization

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/penmon", methods=['POST', 'GET'])
def handle_penmon_view():
    if request.method == 'POST':
        data = request.json

        # Prepare data
        place = data['place']
        latitude = data['latitude']
        altitude = data['altitude']
        prepare_data(place, latitude, altitude)

        # Generate data visualization
        figures = generate_data_visualization(place)

        # Save each figure as an image file
        for i, fig in enumerate(figures):
            fig.savefig(os.path.join(app.static_folder, f'figure{i + 1}.png'))

        # Pass the figures array to the template
        print(figures)
        return render_template('penmon.html', figures=figures)
    return render_template('penmon.html')
