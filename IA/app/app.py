import os
import uuid

external_paths = os.path.abspath(os.path.dirname(__file__))
# Remove /api at the end
external_paths = external_paths[:-4]

import sys

sys.path.append(external_paths)
sys.path.append(external_paths + "/penmon")
sys.path.append(external_paths + "/CNN")

from penmon.meteo_data_preparation import manage_meteorological_data
from penmon.meteo_data_visualization import generate_meteorological_data_visualization
from penmon.vineyards_data_preparation import get_vineyards_list, update_vineyard_details, get_vineyard_details

from flask import Flask, render_template, request, redirect
import tensorflow as tf
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

app = Flask(__name__)

"""
REDIRECT
"""


@app.route("/")
def handle_index_view():
    return redirect("/penmon")


"""
PENMON ROUTES
"""


@app.route("/penmon", methods=['POST', 'GET'])
def handle_penmon_view():
    # Check if data/vineyards.csv exists
    vineyards = get_vineyards_list()

    if request.method == 'POST':
        data = request.json

        # Prepare data
        vineyard = data['vineyard']
        latitude = data['latitude']
        altitude = data['altitude']
        date = data['date']

        current_data = get_vineyard_details(vineyard)
        if current_data["latitude"] != latitude or current_data["altitude"] != altitude:
            # Overwrite data
            manage_meteorological_data(vineyard, float(latitude), int(altitude), True)

            # Update vineyards.csv
            update_vineyard_details(vineyard, latitude, altitude)

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
def handle_penmon_view_vineyard(name: str):
    if request.method == 'POST':
        data = request.json
        return update_vineyard_details(name, data['latitude'], data['altitude'])
    return get_vineyard_details(name)


"""
DISEASES RECOGNITION ROUTES
"""


@app.route("/diseases", methods=['POST', 'GET'])
def handle_diseases_view():
    if request.method == 'POST':
        # Get uploaded image
        uploaded_image = request.files['file']

        # Check if image has valid extension
        if uploaded_image.filename.split('.')[-1].lower() not in ['jpg', 'jpeg', 'png']:
            return {
                "message": "Invalid file extension. Only jpg, jpeg and png are allowed."
            }, 422

        # Generate random name for the image with uuid
        uploaded_image.filename = str(uuid.uuid4()) + '.' + uploaded_image.filename.split('.')[-1].lower()

        # Delete all images inside uploaded-images folder
        for filename in os.listdir(os.path.join(app.static_folder, 'uploaded-images')):
            os.remove(os.path.join(app.static_folder, 'uploaded-images', filename))

        # Save image
        uploaded_image.save(os.path.join(app.static_folder, 'uploaded-images', uploaded_image.filename))

        # Load single image
        image_data = tf.keras.preprocessing.image.load_img(
            os.path.join(app.static_folder, 'uploaded-images', uploaded_image.filename),
            target_size=(160, 160)
        )

        image_data = tf.keras.preprocessing.image.img_to_array(image_data)
        image_data = tf.expand_dims(image_data, axis=0)

        # Preprocess image
        img_preprocessed = preprocess_input(image_data)

        # Load model from static/models
        model = tf.keras.models.load_model(os.path.join(app.static_folder, 'models', 'model_simple.h5'))

        # Predict
        prediction = model.predict(img_preprocessed)
        score = tf.nn.softmax(prediction[0])

        class_labels = ['Black Rot', 'Esca', 'Healthy', 'Leaf Blight']

        confidences = []
        for i in prediction.argsort()[0][-len(class_labels):][::-1]:
            # Append array of dict listing class name and its confidence
            confidences.append({
                "class": class_labels[i],
                "score": "{:.2f}".format(100 * prediction[0][i])
            })

        return {
            "prediction": class_labels[np.argmax(score)],
            "confidences": confidences,
            "image": f"uploaded-images/{uploaded_image.filename}",
        }
    return render_template('diseases.html')


# Configuration for the app to run on the server with command "python app.py"
app.run(host='0.0.0.0', port=81)
