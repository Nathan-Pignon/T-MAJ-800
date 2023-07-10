import os
import shutil
import random


def split_initial_data():
    # Path to the initial_data folder
    initial_data_folder = "initial_data"

    # Path to the data folder
    data_folder = "data"
    os.makedirs(data_folder, exist_ok=True)

    # Create the train, test, and val folders inside the data folder
    train_folder = os.path.join(data_folder, "train")
    test_folder = os.path.join(data_folder, "test")
    val_folder = os.path.join(data_folder, "val")

    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(test_folder, exist_ok=True)
    os.makedirs(val_folder, exist_ok=True)

    # Get a list of subfolders inside the initial_data folder
    subfolders = [f.path for f in os.scandir(initial_data_folder) if f.is_dir()]

    # Iterate over each subfolder
    for subfolder in subfolders:
        # Create subfolders inside the train, test, and val folders
        subfolder_name = os.path.basename(subfolder)
        train_subfolder = os.path.join(train_folder, subfolder_name)
        test_subfolder = os.path.join(test_folder, subfolder_name)
        val_subfolder = os.path.join(val_folder, subfolder_name)

        os.makedirs(train_subfolder, exist_ok=True)
        os.makedirs(test_subfolder, exist_ok=True)
        os.makedirs(val_subfolder, exist_ok=True)

        # Get a list of files inside the current subfolder
        files = [f.name for f in os.scandir(subfolder) if f.is_file()]

        # Calculate the number of files for train, test, and val
        num_files = len(files)
        num_train = int(num_files * 0.9)
        num_test = int(num_files * 0.1)
        num_val = 5  # Fixed number of files for validation

        # Randomly shuffle the files
        random.shuffle(files)

        # Copy files to the train folder
        for file in files[:num_train]:
            src = os.path.join(subfolder, file)
            dst = os.path.join(train_subfolder, file)
            shutil.copy(src, dst)

        # Copy files to the test folder
        for file in files[num_train:num_train + num_test]:
            src = os.path.join(subfolder, file)
            dst = os.path.join(test_subfolder, file)
            shutil.copy(src, dst)

        # Pick 5 random files from train and test folders and copy them to the val folder
        train_files = [f.name for f in os.scandir(train_subfolder) if f.is_file()]
        test_files = [f.name for f in os.scandir(test_subfolder) if f.is_file()]

        random.shuffle(train_files)
        random.shuffle(test_files)

        for file in train_files[:num_val]:
            src = os.path.join(train_subfolder, file)
            dst = os.path.join(val_subfolder, file)
            shutil.copy(src, dst)

        for file in test_files[:num_val]:
            src = os.path.join(test_subfolder, file)
            dst = os.path.join(val_subfolder, file)
            shutil.copy(src, dst)
