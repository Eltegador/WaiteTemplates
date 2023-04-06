import tkinter as tk
from PIL import Image, ImageTk
import os

class ImageViewer(tk.Frame):
    def __init__(self, master, folder_path):
        super().__init__(master)
        self.master = master
        self.folder_path = folder_path
        self.image_files = [
            os.path.join(self.folder_path, file)
            for file in os.listdir(self.folder_path)
            if file.endswith(("jpg", "jpeg", "png", "bmp", "gif"))
        ]
        self.current_image = 0
        self.create_widgets()


    

    def create_widgets(self):
        # Create a Canvas widget to display the images
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Load and resize the images and add them to the Canvas
        self.photos = []
        self.labels = []

        for i, image_file in enumerate(self.image_files):
            # Open and resize the image using Pillow
            image = Image.open(image_file)
            image = image.resize((352, 240))

            # Convert the image to Tkinter format and add it to the Canvas
            photo = ImageTk.PhotoImage(image)
            self.photos.append(photo)
            row = i // 5
            col = i % 5
            x = col * 352 + 90
            y = row * 239 + 30
            self.canvas.create_image(x, y, image=photo, anchor="nw", tags=i + 1)

            # Bind the image to a click event
            self.canvas.tag_bind(i + 1, "<Button-1>", lambda event, image_file=image_file: self.show_fullscreen_image(image_file))

    def show_fullscreen_image(self, image_file):
    # Create a new Toplevel window to display the fullscreen image
        fullscreen_window = tk.Toplevel(self.master)
        fullscreen_window.title("Fullscreen Image")

    # Open the image file from the folder path and display it in a Label widget
        image = Image.open(image_file)
        photo = ImageTk.PhotoImage(image)
        self.photo = photo
        fullscreen_label = tk.Label(fullscreen_window, image=photo)
        fullscreen_label.pack(fill=tk.BOTH, expand=True)

    # Add a Back button to the fullscreen window that destroys the window when clicked
        back_button = tk.Button(fullscreen_window, text="Back", command=fullscreen_window.destroy)
        back_button.pack(side=tk.BOTTOM, pady=10)

    # Add a Customize button to the fullscreen window that saves the RGB values of selected pixel coordinates
        customize_button = tk.Button(fullscreen_window, text="Customize", command=lambda: self.save_pixel_colors(image))
        customize_button.pack(side=tk.BOTTOM, pady=10)

    def show_image(self):
        # Open the current image using Pillow
        image = Image.open(self.image_files[self.current_image])

        # Resize the image to fit the label
        width, height = image.size
        max_width = self.master.winfo_width() - 2000
        max_height = self.master.winfo_height() - 2000
        if width > max_width or height > max_height:
            scale = min(max_width/width, max_height/height)
            image = image.resize((int(scale*width), int(scale*height)))

        # Convert the image to Tkinter format and display it
        photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo

    def show_next_image(self):
        # Increment the current image index and display the next image
        self.current_image = (self.current_image + 1) % len(self.image_files)
        self.show_image()

    def save_pixel_colors(self, image):
        # Get the selected pixel coordinates from the user
        x1, y1 = 430, 250  # Replace these with the pixel coordinates you want to save Face
        x2, y2 = 79, 225  # Replace these with the pixel coordinates you want to save Sec hand
        x3, y3 = 355, 333 # Replace these with the pixel coordinates you want to save Hour marker lumi
        x4, y4 = 591, 330 #Sec marks
        x5, y5 = 351, 153  #logo

    # Get the RGB values of the selected pixels
        pixel1 = image.getpixel((x1, y1))
        pixel2 = image.getpixel((x2, y2))
        pixel3 = image.getpixel((x3, y3))
        pixel4 = image.getpixel((x4, y4))
        pixel5 = image.getpixel((x5, y5))

    # Save the RGB values to a text file
        with open("pixel_colors.txt", "w") as f:
            f.write(f"{pixel1}\n")
            f.write(f"{pixel2}\n")
            f.write(f"{pixel3}\n")
            f.write(f"{pixel4}\n")
            f.write(f"{pixel5}\n")

        


if __name__ == "__main__":
    # Enter the path of the folder containing the images
    folder_path = r"C:/Users/Tego/Python/Images"

    # Create a Tkinter window and ImageViewer widget
    root = tk.Tk()
    image_viewer = ImageViewer(root, folder_path)
    image_viewer.pack(fill=tk.BOTH, expand=True)

    # Run the Tkinter event loop
    root.mainloop()
