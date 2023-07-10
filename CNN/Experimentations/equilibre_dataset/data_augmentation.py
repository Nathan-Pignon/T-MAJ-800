from keras.preprocessing.image import ImageDataGenerator
import os
import numpy as np


def generate_new_train_images(folder, to_augment_class, final_number_images, image_size=(256, 256)):
    directory = os.path.join(folder, to_augment_class)

    count = len(os.listdir(directory))

    # Create a data generator for the images with transformations
    datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    # Calculate the number of additional images needed to balance the dataset
    augmentation_factor = int(np.ceil(final_number_images / count))
    additional_normal_count = augmentation_factor * count - count

    # Generate additional images and save them to the corresponding subfolder
    normal_generator = datagen.flow_from_directory(
        folder,
        batch_size=1,
        target_size=image_size,
        save_to_dir=directory,
        save_format='jpeg',
        save_prefix='augmented_',
        classes=[to_augment_class]
    )

    for i in range(additional_normal_count):
        normal_generator.next()

    # Check the number of images in subfolder
    new_count = len(os.listdir(directory))
    print(f'New {to_augment_class} count: {new_count}')
