from tkinter import filedialog
from tkinter import colorchooser
import cv2
import numpy as np
import tkinter as tk
from tkinter import Tk
import random
from collections import Counter
from PIL import Image
import PIL
import os
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename

# Create a Tkinter root window to hide during file dialog
root = Tk()
root.withdraw()

# Ask the user to select an image file
file_path = askopenfilename(title='Select an image file', filetypes=[('Image files', '*.png;*.jpg;*.jpeg;*.gif')])

# Open the image file
img = Image.open(file_path)

# Get the RGB data from the image
rgb_data = img.convert('RGB').getdata()

# Count the occurrence of each RGB value
rgb_counts = Counter(rgb_data)

# Calculate the total number of pixels in the image
total_pixels = img.width * img.height

# Create a list of tuples containing the RGB value and its percentage in the image
rgb_percentages = [(rgb, count / total_pixels * 100) for rgb, count in rgb_counts.items()]

# Sort the RGB percentages in descending order
rgb_percentages.sort(key=lambda x: x[1], reverse=True)

# Save the top 3 RGB percentages to a text file
output_file_path = 'input.txt'
with open(output_file_path, 'w') as f:
    for rgb, percentage in rgb_percentages[:5]:
        f.write(f'{rgb}\n')

# Show a message box when done
from tkinter.messagebox import showinfo
showinfo(title='Done', message=f'RGB percentages saved to {output_file_path}')

with open('input.txt', 'r') as file:
    lines = file.readlines()

# Remove first and last characters from each line
new_lines = [line[1:-2] + '\n' for line in lines]

with open('input.txt', 'w') as file:
    file.writelines(new_lines)

# Open input file
with open('input.txt', 'r') as f_in:
    # Read input file contents
    contents = f_in.read()

# Remove commas from contents
contents = contents.replace(',', '')

# Open output file
with open('dominant_colors.txt', 'w') as f_out:
    # Write modified contents to output file
    f_out.write(contents)



# Open a file dialog to select an image file
#root = tk.Tk()
#root.withdraw()
file_path = r"C:\\Users\\Tego\\Desktop\\waite2.png"

for j in range(20):
    # Load the image
    image = cv2.imread(file_path)


    # Convert the image to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Define the colors to replace
    with open('C:\\Users\\Tego\\Python\\Ben\\prev_colors.txt', 'r') as f:
        prev_colors = [line.strip() for line in f]
    with open('C:\\Users\\Tego\\Python\\dominant_colors.txt', 'r') as f:
        dominant_colors = [line.strip() for line in f]
    #while len(dominant_colors) < 4:
        dominant_colors += ['255 255 255', '0 0 0']

    for i in range(len(prev_colors)):
        old_color = [int(c) for c in prev_colors[i].split()]
        new_color = [int(c) for c in dominant_colors[i].split()]

        # Replace the old color with the new color
        mask = np.all(image == old_color, axis=-1)
        image[mask] = new_color

    # Resize the image to 1280x720
    image = cv2.resize(image, (720, 480))

    lines = open('C:\\Users\\Tego\\Python\\dominant_colors.txt').readlines()
    random.shuffle(lines)
    open('C:\\Users\\Tego\\Python\\dominant_colors.txt', 'w').writelines(lines)
   
    # Show the edited image
    #cv2.imshow('Edited Image', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    #cv2.waitKey(0)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    #directory = r'C:\\Users\\Tego\\Python\\Images'
    #os.chdir(directory)

    path = f"C:\\Users\\Tego\\Python\\Ben\\templates\\Images\\image_{j}.png"
    #cv2.destroyAllWindows()
    # Save the image in a folder
    cv2.imwrite(path, image)
    
# Set the path of the folder containing pictures
folder_path = r"C:\\Users\\Tego\\Python\\Ben\\templates\\Images"

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


    
if __name__ == "__main__":
    # Enter the path of the folder containing the images
    folder_path = r"C:\\Users\\Tego\\Python\\Ben\\templates\\Images"

    # Run the Tkinter event loop
    root.mainloop()




