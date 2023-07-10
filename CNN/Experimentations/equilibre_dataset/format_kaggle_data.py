import os


def format_kaggle_data():
    # Rename "Grape" folder to "initial_data"
    os.rename("Grape", "initial_data")

    # Get a list of all subfolders in the "initial_data" folder
    subfolders = [folder for folder in os.listdir("initial_data") if os.path.isdir(os.path.join("initial_data", folder))]

    # Iterate over each subfolder
    for folder in subfolders:
        # Remove "Grape___" from the beginning of the folder name
        new_folder_name = folder.replace("Grape___", "")

        # Remove _(what's in parentheses) pattern if present
        if "(" in new_folder_name:
            start_index = new_folder_name.find("_(")
            end_index = new_folder_name.find(")")
            new_folder_name = new_folder_name[:start_index] + new_folder_name[end_index+1:]

        # Convert the folder name to lowercase
        new_folder_name = new_folder_name.lower()

        # Rename the subfolder
        os.rename(os.path.join("initial_data", folder), os.path.join("initial_data", new_folder_name))
