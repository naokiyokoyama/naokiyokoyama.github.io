from datetime import datetime

import yaml


def generate_image_link(full_size_path, caption, col_width, local):
    if local:
        PATH = "/scripts/photography/photos/compressed_resized_images/{path}"
    else:
        PATH = "https://github.com/naokiyokoyama/website_media/blob/master/imgs/photos/{path}?raw=true"
    full_size_path = PATH.format(path=full_size_path)
    # Thumbnail path is same as the full size path, but the name ends with _thumbnail
    path_no_ext, ext = full_size_path.rsplit(".", 1)
    thumbnail_path = f"{path_no_ext}_thumbnail.{ext}"
    return (
        f'            <div class="col-md-{col_width}">\n'
        f'              <a data-fancybox="gallery" data-src="{full_size_path}" data-caption="{caption}">\n'
        f'                <img src="{thumbnail_path}" class="img-responsive img-thumbnail" />\n'
        f"              </a>\n"
        f"            </div>"
    )


def convert_date_to_string(date_string):
    # Parse the date string to a datetime object
    date_obj = datetime.strptime(date_string, "%Y:%m:%d %H:%M:%S")
    # Format the datetime object to "Month Year" string
    return date_obj.strftime("%B %Y")


def generate_html_from_yaml(yaml_file, col_width, local):
    assert 12 % col_width == 0, f"12 must be divisible by col_width ({col_width})"
    num_cols = 12 // col_width

    photos_code = ""

    with open(yaml_file, "r") as file:
        photos = yaml.safe_load(file)

        count = 0

        for full_size_path, details in photos.items():
            caption = details["caption"]
            location = details["location"]
            date_taken = convert_date_to_string(details["date_taken"])
            caption_parts = [i for i in [caption, location, date_taken] if i != ""]
            caption = "<br>".join(caption_parts)

            html_markup = generate_image_link(full_size_path, caption, col_width, local)
            if count % num_cols == 0:
                photos_code += '          <div class="row">\n'
            photos_code += html_markup + "\n"
            if count % num_cols == num_cols - 1:
                photos_code += "          </div>\n"
            count += 1

    with open("photos_template.html") as file:
        template = file.read()

    template = template.replace("<!--PHOTOS-->", photos_code)

    with open("../../photos.html", "w") as file:
        file.write(template[:-1])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate HTML for photos page from YAML file."
    )
    parser.add_argument(
        "-c",
        "--col_width",
        type=int,
        help="The desired width of the thumbnail.",
        default=3,
    )
    parser.add_argument(
        "-l",
        "--local",
        action="store_true",
        help="Use local path for images.",
    )
    args = parser.parse_args()
    if args.local:
        print("WARNING: Using local path for images.")
    generate_html_from_yaml("photos.yaml", args.col_width, args.local)
