import tkinter as tk
from tkinter import ttk
from turtle import width

# Create a new Tk window
root = tk.Tk()

# Set the window size
root.geometry("200x200")

# Create a canvas to draw the progress bar on
canvas = tk.Canvas(root, width=200, height=200)
canvas.pack()

# Draw the progress bar on the canvas
circle = canvas.create_arc(10, 10, 190, 190, start=90, extent=360, fill="lightgrey", style="arc", width=10)
number = canvas.create_text(100, 100, text="0", font=("Arial", 32))

# Set the initial progress
progress = 0

# Update the progress bar and number
def update(new_progress):
    global progress
    progress = new_progress
    canvas.itemconfigure(circle, extent=360 * progress / 100)
    canvas.itemconfigure(number, text=str(progress))

# Set the progress to 50%
for n in (1,100):
    update(n)

# Run the Tk event loop
root.mainloop()