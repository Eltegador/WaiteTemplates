import tkinter as tk
from tkinter import filedialog
from tkinter import colorchooser
import cv2
import numpy as np

# Create a GUI window using Tkinter
root = tk.Tk()
root.withdraw()  # Hide the root window

# Ask the user to select an image file using a file dialog
file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])

# Load the image
img = cv2.imread(file_path)

# Create a window to display the image and get the RGB value of clicked pixels
cv2.namedWindow("image")

# Define a list to store the clicked colors
clicked_colors = []

def get_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        color = img[y, x]
        clicked_colors.append(color)

        # Save the dominant colors to a text file when 3 unique colors have been selected
        if len(set(tuple(c) for c in clicked_colors)) == 3:
            with open('dominnant_colors.txt', 'w') as f:
                for color in clicked_colors:
                    f.write(f"{color[2]} {color[1]} {color[0]}\n")
                f.write("255 255 255\n")
                f.write("0 0 0\n")

            print("Dominant colors saved to dominnant_colors.txt.")
            cv2.destroyAllWindows()

cv2.setMouseCallback("image", get_color)

# Display the image in the window and wait for a key press
cv2.imshow("image", img)
cv2.waitKey(0)

