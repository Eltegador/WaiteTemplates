from PIL import Image
import os

# Set the path of the folder containing pictures
folder_path = r"C:/Users/Tego/Python/Images"

# Set the pixel coordinate to scan
x_coord = 360
y_coord = 270

# Set the path of the image to layer
layer_path = 'C:/Users/Tego/Desktop/Watch Layers/black cropped.png'

# Set the size of the resized layer image
layer_size = (720, 480)

# Set the RGB color threshold for "light" colors
color_threshold = 200

# Loop through each image in the folder
for file_name in os.listdir(folder_path):
    # Open the image and get its RGB values
    image_path = os.path.join(folder_path, file_name)
    image = Image.open(image_path)
    pixel_value = image.getpixel((x_coord, y_coord))

  # Check if the pixel color is "light"
    if sum(pixel_value) / 3 > color_threshold:
        # Open and resize the layer image
        layer = Image.open(layer_path)
        layer = layer.resize(layer_size)

        # Paste the layer image onto the original image
        image.paste(layer, (0, 2), layer)

        # Save the modified image
        image.save(image_path)
