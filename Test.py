import tkinter as tk
from tkinter import ttk

# Import the Image and ImageTk modules to load and display the image
from PIL import Image, ImageTk
root = tk.Tk()
root.geometry("800x480")
root.rowconfigure((0,1), weight=1)  # make buttons stretch when
root.columnconfigure((0,2), weight=1)
# Create a new Tk object

# Load the image files
image1 = Image.open("icons/youtube-play-button.png")
image1 = image1.resize((75,75), Image.ANTIALIAS)
image1 = ImageTk.PhotoImage(image1)

image2 = Image.open("icons/stop-button.png")
image2 = ImageTk.PhotoImage(image2)

# Create three buttons and position them using the grid layout manager
button1 = tk.Button(root, text="Start", bg="green", fg="white", image=image1, compound="left")
button1.grid(row=0, column=0, sticky="NSEW")

# Create a flag variable to keep track of the state of the button
button1_is_clicked = False

# Define a function that changes the state of the button and the image
def change_button1():
    return
    # global button1_is_clicked
    # if button1_is_clicked:
    #     # Change the image to the first image and set the flag to False
    #     button1.config(image=image1, bg="red")
    #     button1_is_clicked = False
    # else:
    #     # Change the image to the second image and set the flag to True
    #     button1.config(image=image2)
    #     button1_is_clicked = True

button2 = tk.Button(root, text="Button 2")
button2.grid(row=0, column=1, sticky="NSEW")

# Bind the function to the button 3
button3 = tk.Button(root, text="Button 3", command=change_button1)
button3.grid(row=0, column=2, sticky="NSEW")



# Start the event loop
root.mainloop()