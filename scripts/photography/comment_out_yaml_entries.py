import os
import yaml
import argparse
from yaml import Dumper


def comment_out_missing_files(yaml_path: str, directory_path: str) -> None:
    # Check if the directory exists
    if not os.path.isdir(directory_path):
        print(f"The directory {directory_path} does not exist.")
        return

    # Load the YAML file
    with open(yaml_path, "r") as file:
        try:
            data = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)
            return

    # Check if each file in the YAML exists in the directory
    modified = False
    for file_name in list(data.keys()):
        file_path = os.path.join(directory_path, file_name)
        if not os.path.isfile(file_path):
            # File does not exist, comment out the entry
            data["# " + file_name] = data.pop(file_name)
            modified = True

    # If modifications have been made, write the commented out data back to the YAML file
    if modified:
        with open(yaml_path, "w") as file:
            yaml.dump(data, file, Dumper=Dumper, sort_keys=False)
            print(
                f"Updated the YAML file {yaml_path} with commented out entries for missing files."
            )
    else:
        print("No missing files. The YAML file was not modified.")


def main() -> None:
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Comment out entries in a YAML file for files missing in a directory"
    )
    parser.add_argument(
        "directory_path",
        type=str,
        help="Path to the directory to check for file existence",
    )
    parser.add_argument("yaml_path", type=str, help="Path to the YAML file to modify")

    # Parse the arguments
    args = parser.parse_args()

    # Call the function with provided arguments
    comment_out_missing_files(args.yaml_path, args.directory_path)


if __name__ == "__main__":
    main()
