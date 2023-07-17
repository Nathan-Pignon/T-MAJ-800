import argparse

from data_preparation import prepare_data
from data_visualization import generate_data_visualization


def parse_args():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Positional mandatory arguments
    parser.add_argument("place", help="Selected place", type=str)
    parser.add_argument("latitude", help="Latitude of the place", type=float)
    parser.add_argument("altitude", help="Altitude of the place", type=int)

    parser.add_argument("-g", "--overwrite-data", help="Overwrite generated data for provided place", type=bool, default=False)

    # Parse arguments
    return parser.parse_args()


if __name__ == "__main__":
    # Catch place, latitude and altitude from arguments when running the script
    # Example: python main.py bordeaux-merignac 44.83986528666804 42
    args = parse_args()

    prepare_data(args.place, args.latitude, args.altitude, args.overwrite_data)
    generate_data_visualization(args.place)
