import zipfile
import os

# Dataset file path
dirname = os.path.dirname(__file__)
DATASET_FILE = os.path.join(dirname, 'data/dataset')

# Cities file path
VINEYARDS_FILE = os.path.join(dirname, 'data/vineyards')


def extract_dataset_file(dataset_file_path: str) -> bool:
    # Unzip data/dataset.zip file
    try:
        with zipfile.ZipFile(f"{dataset_file_path}.zip", "r") as zip_ref:
            zip_ref.extractall("data")
        # Rename data/france_meteo_2014tojuillet2021.csv to data/dataset.csv
        os.rename("data/france_meteo_2014tojuillet2021.csv", f"{dataset_file_path}.csv")

        return True
    except FileNotFoundError:
        return False


def check_dataset_file_exists(dataset_file_path: str) -> bool:
    try:
        open(f"{dataset_file_path}.csv")
        return True
    except FileNotFoundError:
        return False
