import argparse
import os
from PIL import Image
import pathlib
from tqdm import tqdm


def resize_image(pil_image, max_size):
    """Resize the image to a max size, maintaining the aspect ratio."""
    width, height = pil_image.size
    if max(height, width) > max_size:
        scaling_factor = max_size / float(height if height > width else width)
        new_dimensions = (int(width * scaling_factor), int(height * scaling_factor))
        resized_image = pil_image.resize(new_dimensions, Image.LANCZOS)
        return resized_image
    return pil_image


def compress_and_resize_image(image_path, output_folder, quality, max_size):
    """Compress and resize an image, then save it to the output folder."""
    pil_image = Image.open(image_path)
    output_path = os.path.join(output_folder, os.path.basename(image_path))

    # If an image at the output path already exists with the same max_size, skip it
    if os.path.exists(output_path):
        existing_image = Image.open(output_path)
        if max(existing_image.size) == max_size:
            return

    # Preserve EXIF data if present
    exif = pil_image.info["exif"] if "exif" in pil_image.info else None

    if max_size:
        pil_image = resize_image(pil_image, max_size)

    # Save image with EXIF data
    pil_image.save(output_path, "JPEG", quality=quality, exif=exif)


def main(directory, quality, max_size):
    new_directory = os.path.join(directory, "compressed_resized_images")
    pathlib.Path(new_directory).mkdir(parents=True, exist_ok=True)

    # Retrieve all image files
    image_files = [
        file
        for file in os.listdir(directory)
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))
    ]

    # Process each image with a progress bar
    for file in tqdm(image_files, desc="Processing images"):
        file_path = os.path.join(directory, file)
        compress_and_resize_image(file_path, new_directory, quality, max_size)

    print(
        "Images have been compressed and resized (if needed) and saved to "
        f"{new_directory}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compress and optionally resize images in a directory"
    )
    parser.add_argument("directory", type=str, help="Path to the directory with images")
    parser.add_argument(
        "-q", "--quality", type=int, default=85, help="Quality of JPEG compression"
    )
    parser.add_argument(
        "-s", "--size", type=int, help="Maximum size of the image's longer dimension"
    )

    args = parser.parse_args()
    main(args.directory, args.quality, args.size)

# import argparse
# import os
# from PIL import Image
# import pathlib
# import cv2
# from tqdm import tqdm
#
#
# def resize_image(image, max_size):
#     """Resize the image to a max size, maintaining the aspect ratio."""
#     height, width = image.shape[:2]
#     if max(height, width) > max_size:
#         scaling_factor = max_size / float(height if height > width else width)
#         new_dimensions = (int(width * scaling_factor), int(height * scaling_factor))
#         resized_image = cv2.resize(image, new_dimensions, interpolation=cv2.INTER_AREA)
#         return resized_image
#     return image
#
#
# def compress_and_resize_image(image_path, output_folder, quality, max_size):
#     """Compress and resize an image, then save it to the output folder."""
#     image = cv2.imread(image_path)
#     if max_size:
#         image = resize_image(image, max_size)
#     output_path = os.path.join(output_folder, os.path.basename(image_path))
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     pil_image = Image.fromarray(image)
#     pil_image.save(output_path, "JPEG", quality=quality)
#
#
# def main(directory, quality, max_size):
#     new_directory = os.path.join(directory, "compressed_resized_images")
#     pathlib.Path(new_directory).mkdir(parents=True, exist_ok=True)
#
#     # Retrieve all image files
#     image_files = [
#         file
#         for file in os.listdir(directory)
#         if file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))
#     ]
#
#     # Process each image with a progress bar
#     for file in tqdm(image_files, desc="Processing images"):
#         file_path = os.path.join(directory, file)
#         compress_and_resize_image(file_path, new_directory, quality, max_size)
#
#     print(
#         "Images have been compressed and resized (if needed) and saved to "
#         f"{new_directory}"
#     )
#
#
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(
#         description="Compress and optionally resize images in a directory"
#     )
#     parser.add_argument("directory", type=str, help="Path to the directory with images")
#     parser.add_argument(
#         "-q", "--quality", type=int, default=85, help="Quality of JPEG compression"
#     )
#     parser.add_argument(
#         "-s", "--size", type=int, help="Maximum size of the image's longer dimension"
#     )
#
#     args = parser.parse_args()
#     main(args.directory, args.quality, args.size)
