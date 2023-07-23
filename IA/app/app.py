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

from CNN.common.cam import make_gradcam_heatmap, generate_heatmaps

from flask import Flask, render_template, request, redirect
import tensorflow as tf
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

app = Flask(__name__)

"""
REDIRECT
"""

# If dirs static/uploaded-images and static/generated-images do not exist, create them
if not os.path.exists(os.path.join(app.static_folder, 'uploaded-images')):
    os.makedirs(os.path.join(app.static_folder, 'uploaded-images'))

if not os.path.exists(os.path.join(app.static_folder, 'generated-images')):
    os.makedirs(os.path.join(app.static_folder, 'generated-images'))


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

        # Generate random uuid
        random_uuid = str(uuid.uuid4())

        # Delete all images inside generated-images folder
        for filename in os.listdir(os.path.join(app.static_folder, 'generated-images')):
            os.remove(os.path.join(app.static_folder, 'generated-images', filename))

        for key in result["month"]:
            result["month"][key].savefig(os.path.join(app.static_folder, 'generated-images', f'{random_uuid}-month-{key}.png'))
            result["month"][key] = f'generated-images/{random_uuid}-month-{key}.png'

        for key in result["year"]:
            result["year"][key].savefig(os.path.join(app.static_folder, f'generated-images/{random_uuid}-year-{key}.png'))
            result["year"][key] = f'generated-images/{random_uuid}-year-{key}.png'

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
        model_name = request.form['model']

        # Check if image has valid extension
        if uploaded_image.filename.split('.')[-1].lower() not in ['jpg', 'jpeg', 'png']:
            return {
                "message": "Invalid file extension. Only jpg, jpeg and png are allowed."
            }, 422

        # Generate random name for the image with uuid
        uploaded_image.filename = str(uuid.uuid4()) + '.' + uploaded_image.filename.split('.')[-1].lower()

        # Paths
        image_path = os.path.join(app.static_folder, 'uploaded-images', uploaded_image.filename)
        heatmaps_path = os.path.join(app.static_folder, 'uploaded-images', f'heatmaps-{uploaded_image.filename}')

        # Delete all images inside uploaded-images folder
        for filename in os.listdir(os.path.join(app.static_folder, 'uploaded-images')):
            os.remove(os.path.join(app.static_folder, 'uploaded-images', filename))

        # Save image
        uploaded_image.save(image_path)

        # Load single image
        image_data = tf.keras.preprocessing.image.load_img(image_path, target_size=(160, 160))

        image_data = tf.keras.preprocessing.image.img_to_array(image_data)
        image_data = tf.expand_dims(image_data, axis=0)

        # Preprocess image
        img_preprocessed = preprocess_input(image_data)

        # Load model from static/models
        try:
            model = tf.keras.models.load_model(os.path.join(app.static_folder, 'models', f'model_{model_name}.h5'))
        except Exception as e:
            return {
                "message": "Model not found"
            }, 404

        # Predict
        prediction = model.predict(img_preprocessed)
        score = tf.nn.softmax(prediction[0])

        # Remove last layer's softmax
        model.layers[-1].activation = None

        heatmaps = []

        for layer in model.layers:
            if 'Conv2D' == layer.__class__.__name__:
                try:
                    heatmap = make_gradcam_heatmap(img_preprocessed, model, layer.name)
                    if np.isnan(heatmap).any():
                        continue
                    else:
                        heatmaps.append({
                            "layer_name": layer.name,
                            "image": heatmap
                        })
                except Exception as e:
                    continue

        fig = generate_heatmaps(image_path, heatmaps, True)
        # Save fig
        fig.savefig(heatmaps_path, bbox_inches='tight')

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
            "image": f"static/uploaded-images/{uploaded_image.filename}",
            "heatmaps": f"static/uploaded-images/heatmaps-{uploaded_image.filename}"
        }
    return render_template('diseases.html')


# Configuration for the app to run on the server with command "python app.py"
app.run(host='0.0.0.0', port=81)
