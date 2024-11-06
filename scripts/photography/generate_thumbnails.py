import cv2
import os
from pathlib import Path
import argparse


def create_thumbnail(image_path, width, height):
    # Check if thumbnail already exists
    filename, file_extension = os.path.splitext(image_path)
    if "thumbnail" in filename:
        return
    thumbnail_path = f"{filename}_thumbnail{file_extension}"
    if Path(thumbnail_path).is_file():
        # Also check if the thumbnail is the correct size
        thumbnail = cv2.imread(thumbnail_path)
        if thumbnail.shape[1] == width and thumbnail.shape[0] == height:
            print(f"Thumbnail for {image_path} already exists. Skipping...")
            return

    desired_aspect_ratio = width / height

    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not open or find the image {image_path}.")
    if image.shape[0] > image.shape[1]:
        # Add blurry background to any images that are taller than they are long
        image = add_blurred_background(
            image_path, desired_aspect_ratio, blur_strength=80
        )

    image_aspect_ratio = image.shape[1] / image.shape[0]

    # Crop to the desired aspect ratio
    if desired_aspect_ratio > image_aspect_ratio:
        # Crop the top and bottom
        new_height = int(image.shape[1] / desired_aspect_ratio)
        crop_height_start = (image.shape[0] - new_height) // 2
        cropped_image = image[crop_height_start : crop_height_start + new_height, :]
    else:
        # Crop the left and right
        new_width = int(image.shape[0] * desired_aspect_ratio)
        crop_width_start = (image.shape[1] - new_width) // 2
        cropped_image = image[:, crop_width_start : crop_width_start + new_width]

    # Choose interpolation method based on whether the image is being upscaled or downscaled
    if width > cropped_image.shape[1] or height > cropped_image.shape[0]:
        interpolation = cv2.INTER_CUBIC
    else:
        interpolation = cv2.INTER_AREA

    # Resize the image with appropriate interpolation method
    resized_image = cv2.resize(
        cropped_image, (width, height), interpolation=interpolation
    )

    # Save the thumbnail
    cv2.imwrite(thumbnail_path, resized_image)
    print(f"Thumbnail saved to {thumbnail_path}")


def make_thumbnails_in_directory(directory, width, height):
    # Get all image files in directory
    images = Path(directory).glob("*.[pP][nN][gG]")
    images = list(images) + list(Path(directory).glob("*.[jJ][pP][gG]"))
    images = list(images) + list(Path(directory).glob("*.[jJ][pP][eE][gG]"))

    for image_path in images:
        create_thumbnail(str(image_path), width, height)


def add_blurred_background(image_path, target_aspect_ratio=16 / 9, blur_strength=30):
    """
    Takes a portrait image and adds blurred side panels to match the target aspect ratio.

    Args:
        image_path: Path to the input image
        target_aspect_ratio: Desired width/height ratio (default 16:9)
        blur_strength: Strength of the Gaussian blur (default 30)

    Returns:
        Processed image with blurred background
    """
    # Read the image
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Could not read the image: {image_path}")

    height, width = img.shape[:2]
    current_ratio = width / height

    # Only process if image is taller than it is wide
    if current_ratio >= target_aspect_ratio:
        print(f"Warning: Image {image_path} already has desired aspect ratio or wider")
        return img

    # Calculate new width needed to achieve target ratio
    new_width = int(height * target_aspect_ratio)

    # Create background by scaling original image to new width
    scale_factor = new_width / width
    temp_height = int(height * scale_factor)
    background = cv2.resize(img, (new_width, temp_height))

    # Apply strong blur to background
    # Ensure kernel size is odd and at least 3
    kernel_size = max(3, int(blur_strength * 2)) | 1  # Makes sure it's odd
    background = cv2.GaussianBlur(background, (kernel_size, kernel_size), blur_strength)

    # Crop background to match original height
    if temp_height > height:
        start_y = (temp_height - height) // 2
        background = background[start_y : start_y + height]

    # Calculate positions to place original image
    x_offset = (new_width - width) // 2

    # Create final composite
    result = background.copy()
    result[:, x_offset : x_offset + width] = img

    return result


def parse_ratio(ratio_str):
    """Convert ratio string (e.g., '16:9' or '1.77') to float"""
    try:
        if ":" in ratio_str:
            num, den = map(float, ratio_str.split(":"))
            return num / den
        return float(ratio_str)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid ratio format: {ratio_str}. Use either ':' format (e.g., '16:9') "
            "or decimal (e.g., '1.77')"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create thumbnails for all image files in a directory."
    )
    parser.add_argument(
        "directory_path",
        type=str,
        help="The path to the directory containing image files.",
    )
    parser.add_argument("width", type=int, help="The desired width of the thumbnail.")
    parser.add_argument("height", type=int, help="The desired height of the thumbnail.")

    args = parser.parse_args()

    # Validate the directory path
    if not Path(args.directory_path).is_dir():
        raise NotADirectoryError(f"No directory found at {args.directory_path}")

    # Create thumbnails for all images in directory
    make_thumbnails_in_directory(args.directory_path, args.width, args.height)
