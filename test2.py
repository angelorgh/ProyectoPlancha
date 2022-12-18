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

root.rowconfigure(0, weight=1)  # make buttons stretch when
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=2)

root.columnconfigure(1, weight=3)

bgcolor1 = '#1E1D1D'
fgcolor1 = '#FF5757'
root.configure(bg=bgcolor1)
# root.attributes("-fullscreen", True)
poppins = tkFont.Font(family='Poppins', size=15, weight=tkFont.BOLD)
Titlepoppins = tkFont.Font(family='Poppins', size=25, weight=tkFont.BOLD)

# Load the image files
image1 = Image.open("icons/Play.png")
image1 = image1.resize((75,75), Image.ANTIALIAS)
image1 = ImageTk.PhotoImage(image1)

image2 = Image.open("icons/Stop.png")
image2 = image2.resize((75,75), Image.ANTIALIAS)
image2 = ImageTk.PhotoImage(image2)

label1 = tk.Label(root, text="Wrinkless", font=Titlepoppins, bg=bgcolor1, fg=fgcolor1)
label1.grid(row=0, column=0, sticky='N', columnspan=3)

# Create three buttons and position them using the grid layout manager
button1 = tk.Button(root, text="Iniciar", bg=bgcolor1,bd=0, fg="white", image=image1, compound="top", font=poppins, width=75, height=125)#, activebackground=bgcolor1)
button1.place(x=20, rely=0.5,relheight=0.40, relwidth=0.15, anchor='w')
button2 = tk.Button(root, text="Detener", bg=bgcolor1,bd=0, fg="white", image=image2, compound="top", font=poppins, width=75, height=125)#, activebackground=bgcolor1)
button2.place(x=20, rely=0.85, relheight=0.40, relwidth=0.15,anchor='w')

label2 = tk.Label(root, text="Temp", font=Titlepoppins, bg=bgcolor1, fg=fgcolor1)
label2.place(x=20, rely=0.5,relheight=0.40, relwidth=0.15, anchor='e')
value1 = tk.Label(root, text="147°C", font=Titlepoppins, bg=bgcolor1, fg='white')
value1.grid(row=2, column=2, sticky='EN')

label3 = tk.Label(root, text="Estatus", font=Titlepoppins, bg=bgcolor1, fg=fgcolor1)
label3.grid(row=3, column=2, sticky="EN")
value2 = tk.Label(root, text="Ok", font=Titlepoppins, bg=bgcolor1, fg='white')
value2.grid(row=4, column=2, sticky="EN")

# Start the event loop
root.mainloop()