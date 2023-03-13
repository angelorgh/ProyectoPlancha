# from cgitb import text
from logging.handlers import RotatingFileHandler
from random import randint
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
from turtle import color
# Import the Image and ImageTk modules to load and display the image
from PIL import Image, ImageTk
from WrinklessBE.server import WebSocketServer
import asyncio
import WrinklessBE.client as client
import time
from WrinklessBE.AI.Spect_ColorClassifier import SpectColorClassifier


server = WebSocketServer("localhost", 8000)
server.start()
# server = BackEnd()
# server.start()
root = tk.Tk()
root.geometry("800x480")

#test
_job = None


#constants

bgcolor1 = '#1E1D1D'
fgcolor1 = '#FF5757'

poppins = tkFont.Font(family='Poppins', size=15, weight=tkFont.BOLD)
poppins2 = tkFont.Font(family='Poppins', size=25, weight=tkFont.BOLD)
Titlepoppins = tkFont.Font(family='Poppins', size=36, weight=tkFont.BOLD)

# Valor
# estatus =  on_start_click()

def on_start_click():
    global estatus

    value2.config(text='Iniciando')

    timer = asyncio.get_event_loop().run_until_complete(client.send_message("100"))
    
    value2.config(text='Planchando')
    progressbar.start(interval=timer)
    time.sleep(1)
    result = asyncio.get_event_loop().run_until_complete(client.send_message("100"))
    while(result.response != "Termine"):
        result = asyncio.get_event_loop().run_until_complete(client.send_message("200"))
        parsetemp = float("{:.2f}".format(result.temp))
        value1.config(text=f"{parsetemp}°C")
    value1.config(text="")

def cancel():
    global _job
    if _job is not None:
        root.after_cancel(_job)
        _job = None

def goodbye_world():
    print("Stopping Feed")
    cancel()
    button1.configure(command=hello_world)

def hello_world():
    print("Starting Feed")
    button1.configure( command=goodbye_world)
    print_sleep()

def print_sleep():
    global _job
    #foo = randint(4000,7500)
    print("Sleeping", randint(4000,7500))
    _job = root.after(100,print_sleep)

class CircularProgressbar(object):
    def __init__(self, canvas, x0, y0, x1, y1, width=2, start_ang=0, full_extent=360.):
        self.custom_font = tkFont.Font(family="Helvetica", size=23, weight='bold')
        self.canvas = canvas
        self.x0, self.y0, self.x1, self.y1 = x0+width, y0+width, x1-width, y1-width
        self.tx, self.ty = (x1-x0) / 2, (y1-y0) / 2
        self.width = width
        self.start_ang, self.full_extent = start_ang, full_extent
        # draw static bar outline
        w2 = width / 2
        # self.oval_id1 = self.canvas.create_oval(self.x0-w2, self.y0-w2,
        #                                         self.x1+w2, self.y1+w2)
        # self.oval_id2 = self.canvas.create_oval(self.x0+w2, self.y0+w2,
        #                                         self.x1-w2, self.y1-w2)
        self.running = False

    def start(self, interval=100):
        self.interval = interval  # Msec delay between updates.
        self.increment = self.full_extent / interval
        self.extent = 0
        self.arc_id = self.canvas.create_arc(self.x0, self.y0, self.x1, self.y1,
                                             start=self.start_ang, extent=self.extent,
                                             width=self.width, style='arc', outline=fgcolor1)
        percent = '0%'
        
        # Calculate the center of the circle
        cx = (self.x0 + self.x1) / 2
        cy = (self.y0 + self.y1) / 2

        # Create the label at the center of the circle
        self.label_id = self.canvas.create_text(cx, cy, text=percent, font=poppins2, fill='white')

        # self.label_id = self.canvas.create_text(self.tx, self.ty, text=percent,
                                                # font=self.custom_font)
        self.running = True
        self.canvas.after(interval, self.step, self.increment)

    def step(self, delta):
        """Increment extent and update arc and label displaying how much completed."""
        if self.running:
            self.extent = (self.extent + delta) % 360
            self.canvas.itemconfigure(self.arc_id, extent=self.extent)
            # Update percentage value displayed.
            percent = '{:.0f}%'.format(
                                    round(float(self.extent) / self.full_extent * 100))
            self.canvas.itemconfigure(self.label_id, text=percent)
        self.canvas.after(self.interval, self.step, delta)


    def toggle_pause(self):
        self.running = not self.running


root.rowconfigure(0, weight=1)  # make buttons stretch when
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=2)

root.columnconfigure(1, weight=3)
root.config(cursor="none")
root.configure(bg=bgcolor1)
root.attributes("-fullscreen", False)


# Load the image files
image1 = Image.open("icons/Play.png")
image1 = image1.resize((75,75), Image.ANTIALIAS)
image1 = ImageTk.PhotoImage(image1)

image2 = Image.open("icons/Stop.png")
image2 = image2.resize((75,75), Image.ANTIALIAS)
image2 = ImageTk.PhotoImage(image2)

label1 = tk.Label(root, text="Wrinkless", font=Titlepoppins, bg=bgcolor1, fg=fgcolor1, pady=20)
label1.grid(row=0, column=0, sticky='N', columnspan=3)



#  Botones izquierda
button1 = tk.Button(root, text="Iniciar", bg=bgcolor1,bd=0, fg="white", image=image1, compound="top", font=poppins, width=75, height=125, highlightthickness=0, command=on_start_click)
button1.place(x=20, rely=0.5,relheight=0.35, relwidth=0.15, anchor='w')
button2 = tk.Button(root, text="Cancelar", bg=bgcolor1,bd=0, fg="white", image=image2, compound="top", font=poppins, width=75, height=125, highlightthickness=0, command=goodbye_world)
button2.place(x=20, rely=0.85, relheight=0.35, relwidth=0.15,anchor='w')

# CIRCULO PROGESO CENTRO
canvas = tk.Canvas(root, width=250, height=250, bg=bgcolor1, highlightthickness=0)
#canvas.pack(anchor="center")

progressbar = CircularProgressbar(canvas, 20, 20, 230, 230, 25)
canvas.place(rely=0.65,relx=0.54,relheight=0.5, relwidth=0.40, anchor='center')

#progressbar.step(1)

#  Texto derecha
label2 = tk.Label(root, text="Temp", font=poppins2, bg=bgcolor1, fg=fgcolor1)
label2.place(x=-20,relx=1, rely=0.45,relheight=0.20, relwidth=0.20, anchor='e')
value1 = tk.Label(root, text="", font=poppins2, bg=bgcolor1, fg='white')
value1.place(x=-20,relx=1, rely=0.60,relheight=0.20, relwidth=0.20, anchor='e')

label3 = tk.Label(root, text="Estatus", font=poppins2, bg=bgcolor1, fg=fgcolor1)
label3.place(x=-20,relx=1, rely=0.75,relheight=0.20, relwidth=0.20, anchor='e')
value2 = tk.Label(root, text='En Espera',font=poppins2, bg=bgcolor1, fg='white')
value2.place(x=-20,relx=1, rely=0.90,relheight=0.20, relwidth=0.20, anchor='e')



# def sendMessage():
#     message = "0"
#     asyncio.get_event_loop().run_until_complete(client.send_message("100"))

# root.after(50, readSerial)


# Start the event loop
root.mainloop()