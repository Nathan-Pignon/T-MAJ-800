import numpy as np
from PIL import Image, ImageOps
import random
import os


def image_shuffle(image, size):
    # Redimensionner l'image
    img = image.resize(size)

    # Définir la taille des morceaux
    chunk_size = (size[0] // 10, size[1] // 10)  # Ce sera une grille de 10x10

    # Découper l'image
    chunks = [img.crop((i * chunk_size[0], j * chunk_size[1], (i + 1) * chunk_size[0], (j + 1) * chunk_size[1])) for j
              in range(10) for i in range(10)]

    # Mélanger les morceaux
    random.shuffle(chunks)

    # Créer une nouvelle image pour contenir les morceaux
    new_img = Image.new('RGB', size)

    # Recoller les morceaux dans la nouvelle image
    for i, chunk in enumerate(chunks):
        new_img.paste(chunk, (i % 10 * chunk_size[0], i // 10 * chunk_size[1]))

    return new_img


def shuffle_images_in_directories(directory_origin, directory_destination, size):
    for filename in os.listdir(directory_origin):
        filepath = os.path.join(directory_origin, filename)
        image = Image.open(filepath)

        # Appliquer la fonction image_shuffle à chaque image
        #shuffled_image = image_merge_center(filepath, size)
        grid_image = image_merge_grid(filepath, size)

        # Retourner l'image horizontalement et verticalement
        flip_horz_image = ImageOps.flip(grid_image)
        flip_vert_image = ImageOps.mirror(grid_image)

        # Sauvegarder les images dans le même répertoire
        grid_image.save(os.path.join(directory_destination, "grid_"+filename))
        flip_horz_image.save(os.path.join(directory_destination, "grid_horz_"+filename))
        flip_vert_image.save(os.path.join(directory_destination, "grid_vert_"+filename))

        # Sauvegarder la nouvelle image dans le même répertoire
        #image.save(os.path.join(directory_destination, filename))
        #shuffled_image.save(os.path.join(directory_destination, "shuffled_" + filename))
        #grid_image.save(os.path.join(directory_destination, "grid_" + filename))


def choose_random_healthy_image(healthy_images_number):
    directory = "../../../Datas/Grape/HEALTHY/"
    # Obtenir la liste des fichiers
    filenames = os.listdir(directory)

    # Vérifier si le nombre d'images demandé est inférieur ou égal au nombre total d'images disponibles
    if healthy_images_number > len(filenames):
        raise ValueError("The number of images requested is greater than the total number of available images.")

    # Choisir nbImages fichiers au hasard sans remplacement
    random_filenames = random.sample(filenames, healthy_images_number)

    # Retourner les chemins complets des images
    return [os.path.join(directory, filename) for filename in random_filenames]


def image_merge_center(image_path1, size):
    image_path2 = choose_random_healthy_image(1)
    # Charger les images
    img1 = Image.open(image_path1).resize(size)
    img2 = Image.open(image_path2[0]).resize(size)

    # Définir la taille des morceaux
    chunk_size = (size[0] // 4, size[1] // 4)

    # Découper les images
    chunks1 = [
        [img1.crop((i * chunk_size[0], j * chunk_size[1], (i + 1) * chunk_size[0], (j + 1) * chunk_size[1])) for i in
         range(4)] for j in range(4)]
    chunks2 = [
        [img2.crop((i * chunk_size[0], j * chunk_size[1], (i + 1) * chunk_size[0], (j + 1) * chunk_size[1])) for i in
         range(4)] for j in range(4)]

    # Créer une nouvelle image pour contenir les morceaux
    new_img = Image.new('RGB', size)

    # Coller les morceaux dans la nouvelle image
    for j in range(4):
        for i in range(4):
            if ((i == 0 and j == 0) or (i == 0 and j == 3) or (i == 3 and j == 0) or (
                    i == 3 and j == 3)):  # Les 4 carrés de chaque coins de l'image 1
                # Utiliser les carrés centraux de l'image 2
                if (i == 0 and j == 0):
                    chunk = chunks2[1][1]  # Top-left corner
                elif (i == 3 and j == 0):
                    chunk = chunks2[1][2]  # Top-right corner
                elif (i == 0 and j == 3):
                    chunk = chunks2[2][1]  # Bottom-left corner
                else:  # (i == 3 and j == 3)
                    chunk = chunks2[2][2]  # Bottom-right corner
            else:  # Tous les autres carrés de l'image 1
                chunk = chunks1[j][i]
            new_img.paste(chunk, (i * chunk_size[0], j * chunk_size[1]))

    return image_shuffle(new_img, size)


def image_merge_grid(image_path, size, healthy_images_number=3):
    # Charger l'image actuelle
    main_img = Image.open(image_path).resize(size)

    # Obtenir les chemins d'accès des images saines
    healthy_images_paths = choose_random_healthy_image(healthy_images_number)

    # Ajouter le chemin d'accès de l'image actuelle aux chemins d'accès des images saines
    image_paths = healthy_images_paths + [image_path]

    # Mélanger les chemins d'accès des images
    random.shuffle(image_paths)

    # Définir la taille de chaque image dans la grille (toutes les images auront la même taille)
    grid_image_size = (size[0] // 2, size[1] // 2)

    # Créer une nouvelle image pour contenir la grille
    new_img = Image.new('RGB', size)

    # Copier chaque image sur l'image de la grille
    for i, image_path in enumerate(image_paths):
        # Charger l'image
        img = Image.open(image_path).resize(grid_image_size)

        # Définir la position à laquelle l'image sera collée sur l'image de la grille
        x = (i % 2) * grid_image_size[0]
        y = (i // 2) * grid_image_size[1]

        # Coller l'image sur l'image de la grille
        new_img.paste(img, (x, y))

    return new_img
