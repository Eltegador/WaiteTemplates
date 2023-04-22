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
import pyodbc
import base64
import pandas as pd
import io
import matplotlib.pyplot as plt
import uuid
from flask import Flask, Response, jsonify, render_template, request, send_file


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/customize", methods=["POST"])
def customize():
    # establish a connection to the database
    connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:waiteconfigurator.database.windows.net,1433;Database=waiteconfigurator-database;Uid=CloudSA4957129b;Pwd={duvhjndbvosdgg77$};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    connection = pyodbc.connect(connection_string)
    # create a cursor to execute SQL queries
    cursor = connection.cursor()

    # Create a Tkinter root window to hide during file dialog
    root = Tk()
    root.withdraw()

    # Get the uploaded file
    file_path = request.files['image']

    # Ask the user to select an image file
    #file_path = askopenfilename(title='Select an image file', filetypes=[('Image files', '*.png;*.jpg;*.jpeg;*.gif')])

    # Open the image file
    img = Image.open(file_path)

    sub_name = uuid.uuid4()

    query = 'INSERT INTO dbo.SUBMISSIONS VALUES (?)'
    cursor.execute(query, (sub_name))

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

    dominant_list = [] 
    for rgb, percentage in rgb_percentages[:5]:
        dominant_list.append(rgb)
        dominant_list = [str(x).replace(',', '').replace('(', '').replace(')', '') for x in dominant_list]
        print (dominant_list)
        
    file_path = pd.read_sql_query("SELECT TEMPLATE_DATA FROM dbo.TEMPLATE", connection)
    data = (file_path.iloc[0,0])
    # Load the image
    # Create a bytes IO object from the raw data
    image_io = io.BytesIO(data)
    # Use PIL to open the image from the bytes IO object
    image_dat = Image.open(image_io)
    PREFINALimage = np.array(image_dat)
    # convert the image to RGB
    image_dat = image_dat.convert('RGB')
    image2 = cv2.cvtColor(PREFINALimage, cv2.COLOR_RGB2BGR)
    previous_colors = ["128 133 140", "107 106 107", "72 80 72", "90 90 100", "255 255 254"]
    images_no_logo = []

    for j in range(20):   
        image = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
        # Define the colors to replace
      
        while len(dominant_list) < 4:
            dominant_list += ['255 255 255', '0 0 0']
        #print(dominant_list)
        for i in range(len(previous_colors)):
            old_color = [int(c) for c in previous_colors[i].split()]
            new_color = [int(c) for c in dominant_list[i].split()]

        # Replace the old color with the new color
            mask = np.all(image == old_color, axis=-1)
            image[mask] = new_color
        
        # Resize the image to 1280x720
        image = cv2.resize(image, (1080, 720))

        random.shuffle(dominant_list)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        images_no_logo.append(image)

    images_with_logo = []

    # Set the pixel coordinate to scan
    x_coord = 360
    y_coord = 270

    # Set the path of the image to layer
    layer_path = pd.read_sql_query("SELECT LOGO_DATA FROM dbo.LOGO", connection)
    logo_data = (layer_path.iloc[0,0])
    logo_io = io.BytesIO(logo_data)
    # Use PIL to open the image from the bytes IO object
    logo_dat = Image.open(logo_io)
    logo = np.array(logo_dat)
    logo_dat = logo_dat.convert('RGBA')

    #print (data)

    # Set the size of the resized layer image
    layer_size = (1080, 720)

    # Set the RGB color threshold for "light" colors
    color_threshold = 200
    i = 0
    # Loop through each image in the folder
    for img in images_no_logo :
        # Open the image and get its RGB values
        i += 1
        image = Image.fromarray(img)
        pixel_value = image.getpixel((x_coord, y_coord))

        # Check if the pixel color is "light"
        if sum(pixel_value) / 3 > color_threshold:
            # Open and resize the layer image
            logo_dat = logo_dat.resize(layer_size)
            # Paste the layer image onto the original image
            image.paste(logo_dat, (0, 4), logo_dat)
            # insert the image data into the database
            image = np.array(image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            images_with_logo.append(image)

            image_data = image.tobytes()

            cursor.execute('''SELECT MAX(SUB_ID) FROM dbo.SUBMISSIONS WHERE SUB_NAME = ?''', sub_name)
            sub_id = cursor.fetchone()[0]

            cursor.execute('''INSERT INTO dbo.IMAGES (SUB_ID, IMAGE_NAME, IMAGE_DATA)VALUES (?, ?, ?)''', (sub_id, 'image_{i}.png', image_data))
            connection.commit()
        else:
            image = np.array(image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            images_with_logo.append(image)

            image_data = image.tobytes()

            cursor.execute('''SELECT MAX(SUB_ID) FROM dbo.SUBMISSIONS WHERE SUB_NAME = ?''', sub_name)
            sub_id = cursor.fetchone()[0]
        
            cursor.execute('''INSERT INTO dbo.IMAGES (SUB_ID, IMAGE_NAME, IMAGE_DATA)VALUES (?, ?, ?)''', (sub_id, 'image_{i}.png', image_data))
            connection.commit()
    cursor.close()
    connection.close()
            
    images_with_logo = [Image.fromarray(img) for img in images_with_logo]
    
    # Create a bytes IO object to hold the image data
    images_io = [io.BytesIO() for _ in range(len(images_with_logo))]
    
    # Save each image to a separate bytes IO object in PNG format
    for i, img in enumerate(images_with_logo):
        img.save(images_io[i], 'PNG')
        images_io[i].seek(0)
    
    # Encode each image as a Base64 string
    new_image_data = []
    for image_io in images_io:
        image_base64 = base64.b64encode(image_io.getvalue()).decode('utf-8')
        new_image_data.append(image_base64)
    
    # Return the new image data as a JSON response
    return render_template("customize.html", images=new_image_data)

    

    

   
    
@app.route('/processed', methods=['POST'])
def processed():

    response = Response(customize(), mimetype='application/json')
    
    # Convert the Response object to JSON-serializable data
    data = {
        'status': response.status,
        'headers': dict(response.headers),
        'data': response.get_data().decode('utf-8')
    }
    
    # Return the JSON-serializable data as a JSON response
    return jsonify(data)



if __name__ == "__main__":
    	app.run(debug=True)
