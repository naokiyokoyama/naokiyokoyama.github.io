import datetime

from typing import Optional
from PIL import Image
from PIL.ExifTags import TAGS

import os
from tqdm import tqdm
import yaml
import argparse


def get_image_date_taken(image_path: str) -> Optional[str]:
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        if exif_data is None:
            return ""
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            if tag_name == "DateTimeOriginal":
                return value
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""


def generate_yaml(directory: str, yaml_path: str):
    existing_data = {}
    if os.path.exists(yaml_path):
        with open(yaml_path, "r") as file:
            existing_data = yaml.safe_load(file) or {}

    image_files = [
        file
        for file in os.listdir(directory)
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))
        and "thumbnail" not in file.lower()
    ]

    photos = {}
    for file in tqdm(image_files, desc="Processing images"):
        if file not in existing_data:
            file_path = os.path.join(directory, file)
            date_taken = get_image_date_taken(file_path)
            photos[file] = {"date_taken": date_taken, "caption": "", "location": ""}

    existing_data.update(photos)

    # Convert the date_taken to a sortable format and sort the items
    sortable_items = []
    for file_name, data in existing_data.items():
        date_taken = data.get("date_taken", "")
        # Handle the format of the date string if it's not in the correct format
        try:
            taken_datetime = datetime.datetime.strptime(date_taken, "%Y:%m:%d %H:%M:%S")
        except ValueError:
            # If there's a ValueError, which means the date is not in the expected format, we'll use a default date far in the past.
            taken_datetime = datetime.datetime.min
        sortable_items.append((file_name, taken_datetime, data))

    # Sort the items by the date taken (descending)
    sorted_items = sorted(sortable_items, key=lambda x: x[1])[::-1]

    # Reconstruct the sorted data
    sorted_data = {item[0]: item[2] for item in sorted_items}

    with open(yaml_path, "w") as file:
        yaml.dump(sorted_data, file, sort_keys=False)

    print(f"YAML file saved to {yaml_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a YAML file with details of every photo in a directory."
    )
    parser.add_argument("directory", type=str, help="Path to the directory with images")
    parser.add_argument(
        "yaml_path", type=str, help="Path where the YAML file will be saved"
    )
    args = parser.parse_args()

    generate_yaml(args.directory, args.yaml_path)
