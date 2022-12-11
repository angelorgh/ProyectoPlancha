from cgitb import text
from logging.handlers import RotatingFileHandler
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
from turtle import color

# Import the Image and ImageTk modules to load and display the image
from PIL import Image, ImageTk
root = tk.Tk()
root.geometry("800x480")



root.rowconfigure((0,1), weight=1)  # make buttons stretch when
root.columnconfigure((0,2), weight=1)
bgcolor1 = '#1E1D1D'
fgcolor1 = '#FF5757'
root.configure(bg=bgcolor1)
# root.attributes("-fullscreen", True)
poppins = tkFont.Font(family='Poppins', size=15, weight=tkFont.BOLD)
Titlepoppins = tkFont.Font(family='Poppins', size=25, weight=tkFont.BOLD)
# Create a new Tk object

# Load the image files
image1 = Image.open("icons/Play.png")
image1 = image1.resize((75,75), Image.ANTIALIAS)
image1 = ImageTk.PhotoImage(image1)

image2 = Image.open("icons/Stop.png")
image2 = image2.resize((75,75), Image.ANTIALIAS)
image2 = ImageTk.PhotoImage(image2)

# Create label for tittle
# frame=tk.Frame(root, width=300, height=300)
# frame.grid(row=0, column=0, sticky="N")
label1 = tk.Label(root, text="Wrinkless", font=Titlepoppins, bg=bgcolor1, fg=fgcolor1)
label1.grid(row=0, column=0, sticky='N', columnspan=3)
# label1.place(anchor='center')

# Create three buttons and position them using the grid layout manager
button1 = tk.Button(root, text="Iniciar", bg=bgcolor1,bd=0, fg="white", image=image1, compound="top", font=poppins)#, activebackground=bgcolor1)
button1.grid(row=1, column=0, sticky="NWES")
button2 = tk.Button(root, text="Detener", bg=bgcolor1,bd=0, fg="white", image=image2, compound="top", font=poppins)#, activebackground=bgcolor1)
button2.grid(row=2, column=0, sticky="NWES")

button3 = tk.Button(root, text="Iniciar", bg=bgcolor1,bd=0, fg="white", image=image1, compound="top", font=poppins)#, activebackground=bgcolor1)
button3.grid(row=1, column=3, sticky="NWES")
button4 = tk.Button(root, text="Detener", bg=bgcolor1,bd=0, fg="white", image=image2, compound="top", font=poppins)#, activebackground=bgcolor1)
button4.grid(row=2, column=3, sticky="NWES")
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



# # Bind the function to the button 3
# button3 = tk.Button(root, text="Button 3", command=change_button1)
# button3.grid(row=0, column=2, sticky="NSEW")



# Start the event loop
root.mainloop()