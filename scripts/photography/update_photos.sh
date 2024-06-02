# Use this bash script with "--local" to use local directory of images

echo "Compressing and resizing images in photos/..."
python compress_images.py photos/ -q 75 -s 4000 &&
# Remove any files in photos/compressed_resized_images/ that are not in photos/
for f in photos/compressed_resized_images/*; do
  # Skip files with "thumbnail" in the name
  if [[ $(basename $f) == *"thumbnail"* ]]; then
    continue
  fi

  if [ ! -f photos/$(basename $f) ]; then
    rm $f
    echo "Removed $f"
    # remove the thumbnail as well
    rm -f photos/compressed_resized_images/$(basename $f | sed 's/\./_thumbnail\./')
    echo "Removed photos/compressed_resized_images/$(basename $f | sed 's/\./_thumbnail\./')"
  fi
done &&
echo "Generating thumbnails..."
python generate_thumbnails.py photos/compressed_resized_images/ 320 240 &&
# python comment_out_yaml_entries.py photos/compressed_resized_images photos.yaml &&
echo "Generating photos.yaml..."
python generate_photos_yaml.py photos/compressed_resized_images/ photos.yaml &&
echo "Generating photos.html..."
python generate_photos_html.py -c 4 $1
