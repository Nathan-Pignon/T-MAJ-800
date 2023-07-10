import os
import numpy as np
from PIL import Image


# Function to load and resize images from a folder
def load_images_from_folder(folder, img_width, img_height):
    X = []
    y = []

    # Get a list of all subfolders in the folder
    subfolders = [subfolder for subfolder in os.listdir(folder) if os.path.isdir(os.path.join(folder, subfolder))]

    for subfolder in subfolders:
        folder_path = os.path.join(folder, subfolder)
        for filename in os.listdir(folder_path):
            img_path = os.path.join(folder_path, filename)
            img = Image.open(img_path)

            # Resize the image to the desired size
            img = img.resize((img_width, img_height))

            # Convert RGB image to grayscale
            img = img.convert('L')

            # Convert the image to a NumPy array and append it to X
            img = np.array(img)
            X.append(img)

            # Append the corresponding label to y
            y.append(subfolders.index(subfolder))

    X = np.array(X)
    y = np.array(y)
    return X, y