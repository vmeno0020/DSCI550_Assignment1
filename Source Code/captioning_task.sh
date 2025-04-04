# !/bin/bash
# Step 1: Unzip the PNG images to the specified directory
unzip -o ./image/pathway/.zip -d /new/image/pathway/
# Step 2: Create the Python script to convert PNG to JPG
cat > convert_png_to_jpg.py <<EOF
import os
from PIL import Image
# Define input and output directories
input_dir = “./images/”
output_dir = “/jpeg_images/”
# Create output directory if it doesn’t exist
os.makedirs(output_dir, exist_ok=True)
# Loop through all files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(‘.png’):  # Process only PNG files
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename.replace(‘.png’, ‘.jpg’))
        # Open image and convert to JPEG
        img = Image.open(input_path).convert(“RGB”)
        img.save(output_path, “JPEG”)
print(“Conversion complete! JPEGs saved in:“, output_dir)
EOF
# Step 3: Run the Python script to convert PNG to JPG
python3 convert_png_to_jpg.py
# Step 4: Send each JPG file to the server for captioning using curl
for file in ./jpeg_images/*.jpg; do
    echo “Processing $file...”
    curl -X POST “http://localhost:8764/inception/v3/caption/image” --data-binary @$file
done
# Step 5: Create a .tsv file and add captions for each image
echo -e “Filename\tCaption” > /captions/.tsv
for file in ./jpeg_images/*.jpg; do
    echo “Processing $file...”
    caption=$(curl -X POST “http://localhost:8764/inception/v3/caption/image” --data-binary @$file)
    echo -e “$(basename $file)\t$caption” >> /captions/.tsv
done
echo “Process complete! Captions saved in /captions/.tsv”