import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import random
from PIL import Image
import PIL
import os

# Open a file dialog to select an image file
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(title='Select an image', filetypes=(('Image files', '*.jpg;*.jpeg;*.png'), ('All files', '*.*')))

for j in range(20):
    # Load the image
    image = cv2.imread(file_path)


    # Convert the image to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Define the colors to replace
    with open('C:\\Users\\Tego\\Python\\prev_colors.txt', 'r') as f:
        prev_colors = [line.strip() for line in f]
    with open('C:\\Users\\Tego\\Python\\Ben\\dominnant_colors.txt', 'r') as f:
        dominant_colors = [line.strip() for line in f]
    while len(dominant_colors) < 4:
        dominant_colors += ['255 255 255', '0 0 0']

    for i in range(len(prev_colors)):
        old_color = [int(c) for c in prev_colors[i].split()]
        new_color = [int(c) for c in dominant_colors[i].split()]

        # Replace the old color with the new color
        mask = np.all(image == old_color, axis=-1)
        image[mask] = new_color

    # Resize the image to 1280x720
    image = cv2.resize(image, (720, 480))

    lines = open('C:\\Users\\Tego\\Python\\Ben\\dominnant_colors.txt').readlines()
    random.shuffle(lines)
    open('C:\\Users\\Tego\\Python\\ben\\dominnant_colors.txt', 'w').writelines(lines)
   
    # Show the edited image
    #cv2.imshow('Edited Image', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    #cv2.waitKey(0)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    #directory = r'C:\\Users\\Tego\\Python\\Images'
    #os.chdir(directory)

    path = f"C:\\Users\\Tego\\Python\\Images\\image_{j}.png"
    #cv2.destroyAllWindows()
    # Save the image in a folder
    cv2.imwrite(path, image)
    
