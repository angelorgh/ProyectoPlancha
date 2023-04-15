import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
from turtle import color
from PIL import Image, ImageTk
from WrinklessBE.server import WebSocketServer
import asyncio
import WrinklessBE.client as client
import time
from WrinklessBE.calibration import Calibration
import subprocess

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.bgcolor1 = '#1E1D1D'
        self.fgcolor1 = '#FF5757'
        self.poppins = tkFont.Font(family='Poppins', size=15, weight=tkFont.BOLD)
        self.poppins2 = tkFont.Font(family='Poppins', size=19, weight=tkFont.BOLD)
        self.Titlepoppins = tkFont.Font(family='Poppins', size=36, weight=tkFont.BOLD)
        self.id = None
        self.id2 = None
        self.start_procedure()
        self.create_widgets()
        self.calibrate()
        self.emergencystop()
    
    def start_procedure (self):
        server = WebSocketServer("localhost", 8000)
        server.start()
        self.master.geometry("800x480")
    
    def create_widgets_circleprogress(self):
        #region CIRCULO PROGESO CENTRO
        self.canvas = tk.Canvas(self.master, width=250, height=250, bg=self.bgcolor1, highlightthickness=0)

        self.progressbar = CircularProgressbar(self.canvas, 20, 20, 230, 230, 25)
        self.canvas.place(rely=0.65,relx=0.54,relheight=0.5, relwidth=0.40, anchor='center')
        #endregion CIRCULO PROGESO CENTRO
    
    def delete_widgets_circleprogress(self):
        self.canvas.destroy()
        self.canvas = None
        self.progressbar = None

    def create_widgets(self):
        self.master.rowconfigure(0, weight=1)  # make buttons stretch when
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=2)

        self.master.columnconfigure(1, weight=3)
        self.master.config(cursor="none")
        self.master.configure(bg=self.bgcolor1)
        self.master.attributes("-fullscreen", False)


        #region Load the image files
        self.image1 = ImageTk.PhotoImage(Image.open("icons/Play.png").resize((75,75), Image.ANTIALIAS))
        self.image2 = ImageTk.PhotoImage(Image.open("icons/Stop.png").resize((75,75), Image.ANTIALIAS))

        #region old code:
            # self.image1 = Image.open("icons/Play.png")
            # self.image1 = self.image1.resize((75,75), Image.ANTIALIAS)
            # self.image1 = ImageTk.PhotoImage(self.image1)
            # self.image2 = Image.open("icons/Stop.png")
            # self.image2 = self.image2.resize((75,75), Image.ANTIALIAS)
            # self.image2 = ImageTk.PhotoImage(self.image2)
        #endregion old code
        #endregion Load the image files

        #region Titulo
        self.label1 = tk.Label(self.master, text="Wrinkless", font=self.Titlepoppins, bg=self.bgcolor1, fg=self.fgcolor1, pady=20)
        self.label1.grid(row=0, column=0, sticky='N', columnspan=3)
        #endregion Titulo

        #region CIRCULO PROGESO CENTRO
        self.create_widgets_circleprogress()
        #endregion CIRCULO PROGESO CENTRO

        #region  Botones izquierda
        self.button1 = tk.Button(self.master, text="Iniciar", bg=self.bgcolor1,bd=0, fg="white", image=self.image1, compound="top", font=self.poppins, width=75, height=125, highlightthickness=0, command=self.on_start_click)
        self.button1.place(x=20, rely=0.5,relheight=0.35, relwidth=0.15, anchor='w')
        self.button2 = tk.Button(self.master, text="Cancelar", bg=self.bgcolor1,bd=0, fg="white", image=self.image2, compound="top", font=self.poppins, width=75, height=125, highlightthickness=0, command=self.on_cancel_click)
        self.button2.place(x=20, rely=0.85, relheight=0.35, relwidth=0.15,anchor='w')
        #endregion  Botones izquierda

        #region  Texto derecha
        self.label2 = tk.Label(self.master, text="Temp", font=self.poppins2, bg=self.bgcolor1, fg=self.fgcolor1)
        self.label2.place(x=-20,relx=1, rely=0.45,relheight=0.20, relwidth=0.20, anchor='e')
        self.value1 = tk.Label(self.master, text="", font=self.poppins2, bg=self.bgcolor1, fg='white')
        self.value1.place(x=-20,relx=1, rely=0.60,relheight=0.20, relwidth=0.20, anchor='e')

        self.label3 = tk.Label(self.master, text="Estatus", font=self.poppins2, bg=self.bgcolor1, fg=self.fgcolor1)
        self.label3.place(x=-20,relx=1, rely=0.75,relheight=0.20, relwidth=0.20, anchor='e')
        self.value2 = tk.Label(self.master, text='En Espera',font=self.poppins2, bg=self.bgcolor1, fg='white')
        self.value2.place(x=-20,relx=1, rely=0.90,relheight=0.20, relwidth=0.20, anchor='e')
        #endregion  Texto derecha

    def on_start_click(self):
        if self.canvas == None:
            print("Se creo el circulo de nuevo")
            self.create_widgets_circleprogress()
            print(f"Se creo el circulo correctamente. Canvas: {self.canvas} - Circulo: {self.progressbar}")

        self.value2.config(text='Iniciando')
        self.timer = None
        self.progress_window = None
        self.timer = asyncio.get_event_loop().run_until_complete(client.send_message("200"))
        if self.timer == "Nocolor":
            answer5 = tk.messagebox.showwarning(title= 'Cancelado', message = "No se detecto ninguna ropa")
            if answer5 == 'ok':
                return
        self.progress_window = tk.Toplevel(self.master)
        # Center the window on the screen
        x_pos = (self.progress_window.winfo_screenwidth() - self.progress_window.winfo_reqwidth()) // 2
        y_pos = (self.progress_window.winfo_screenheight() - self.progress_window.winfo_reqheight()) // 2
        self.progress_window.geometry("+{}+{}".format(x_pos, y_pos)) 
        self.progress_window.title('Calentando')
        self.progress_bar1 = ttk.Progressbar(self.progress_window, mode='indeterminate', length=300)
        self.progress_bar1.pack(padx=10, pady=10)

        if self.timer == '-1':
            self.emergencystop(self.timer)
        if self.timer.split("%")[1] == 'Calentando':
            print(f"Entro a calentando directamente: {self.timer}")
            self.value2.config(text='Calentando') #NUEVO NO PROBADO
            self.progress_bar1.start()
            self.warmingup()
        else:
            print(f"Entro a planchando directamente: {self.timer}")
            self.timer = int(self.timer.split("%")[0])
            print(self.timer)
            self.value2.config(text='Operando')
            self.progressbar.start(interval=self.timer)
            print('Empezo el progress bar')
            self.callTemperature()

    def on_cancel_click(self):
        self.button1.config(state='disable')
        self.button2.config(state='disable')
        self.value2.config(text="Cancelando")
        if self.id != None:
            print(f"Se va a cancelar el calltemperature: {self.id}")
            self.master.after_cancel(self.id)
            self.id = None
        if self.id2 != None:
            print(f"Se va a cancelar el warmingup: {self.id2}")
            self.master.after_cancel(self.id2)
            self.id2 = None
        result_cancel = asyncio.get_event_loop().run_until_complete(client.send_message("600"))
        print(result_cancel)
        if result_cancel == -1 or result_cancel == '-1':
            self.emergencystop(result_cancel)
        self.delete_widgets_circleprogress()
        if result_cancel == 'Waitingstart':
            answerCancel = tk.messagebox.showinfo(title= 'Cancelado', message = "Se cancelo exitosamente")
            if answerCancel == 'ok':
                self.button1.config(state='normal')
                self.button2.config(state='normal')
                self.value1.config(text="")
                self.value2.config(text="En Espera")

    def warmingup (self):
        resultwarmingup = asyncio.get_event_loop().run_until_complete(client.send_message("500"))
        print(f"Valor lectura: {resultwarmingup}")
        if resultwarmingup == '':
            self.id2 = self.master.after(1000, self.warmingup)
        if resultwarmingup != '':
            print(f"Valor diferente: {resultwarmingup}")
        if resultwarmingup == -1 or resultwarmingup == '-1': 
            self.emergencystop(resultwarmingup)
        if resultwarmingup.strip() == 'Planchando':
            print(f"Entro a planchando valor de result:{resultwarmingup}, timer: {self.timer}, progress: {self.progress_window}")
            self.progress_window.destroy()
            self.timer = int(self.timer.split("%")[0])
            print(self.timer)
            self.value2.config(text='Operando')
            self.progressbar.start(interval=self.timer)
            print('Empezo el progress bar')
            print(f"Se va a cancelar el warmingup: {self.id2}")
            self.master.after_cancel(self.id2)
            self.callTemperature()

    def callTemperature (self):
        self.id
        print(f"Sigue corriendo. Valor {self.progressbar.running}")
        try:
            result = asyncio.get_event_loop().run_until_complete(client.send_message("300"))
            if result == '-1':
                self.emergencystop(result)
            parsetemp = float("{:.2f}".format(float(result.split("%")[0])))
            self.value1.config(text=f"{parsetemp}°C")
            if self.progressbar.running:
                print(f"Keep running")
                self.id = self.master.after(1000, self.callTemperature)
                print(self.id)
            else:
                print(f"CANCEL: {self.id}")
                self.master.after_cancel(self.id)
                self.finishrunnig()
        except Exception as e:
            print(f"ERORR: {e}")

    def calibrate(self):
        self.button1.config(state='disable')
        self.button2.config(state='disable')
        getcalibration = Calibration()
        calibrated = getcalibration.calibrate()

        if(calibrated.find('ERROR') != -1):
            answer = tk.messagebox.askretrycancel(title= 'ERROR!', message = calibrated)
            if answer:
                self.calibrate()
            else:
                self.master.quit()
        else:
            answer2 = tk.messagebox.showinfo(title= 'Calibrated', message = calibrated)
            if answer2== 'ok':
                Honning = asyncio.get_event_loop().run_until_complete(client.send_message("100"))
                if isinstance(Honning, Exception) or Honning.find('Stop') != -1 or Honning == '':
                    answer3 = tk.messagebox.askretrycancel(title= 'ERROR!', message = 'Error in Homing!')
                    if answer3:
                        self.calibrate()
                    else:
                        self.master.quit()
                else:
                    self.button1.config(state='normal')
                    self.button2.config(state='normal')
                    tk.messagebox.showinfo(title= 'READY', message = 'Homing completed')

    def emergencystop (self, wasreceived = ''):
        if wasreceived == '':
            wasreceived = asyncio.get_event_loop().run_until_complete(client.send_message("400"))
            # print(f'Valor de letura de arduino para emergencia: {wasreceived}')
        if wasreceived == -1 or wasreceived == '-1':
            print(f'Valor de parametro para emergencia: {wasreceived}')
            emergencystopbutton = tk.messagebox.showwarning(title = 'EMERGENCY!', message = "SE PRESIONO BOTON DE EMERGENCIA. \n Se cerrara el programa")
            if emergencystopbutton == 'ok':
                self.master.quit()
                # script_path = "/home/pi/Desktop/run_HMI.sh"
                # # run the shell script
                # subprocess.call(script_path, shell=True)
        self.master.after(2000,self.emergencystop)

    def finishrunnig(self):
        finishbutton = tk.messagebox.showinfo(title = 'FINISHED!', message = 'Se termino el planchado')
        if finishbutton == 'ok':
            self.delete_widgets_circleprogress()

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
        fgcolor1 = '#FF5757'
        poppins2 = tkFont.Font(family='Poppins', size=23, weight=tkFont.BOLD)
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
        percent = None
        if self.running:
            self.extent = (self.extent + delta) % 360
            self.canvas.itemconfigure(self.arc_id, extent=self.extent)
            # Update percentage value displayed.
            percent = '{:.0f}%'.format(
                                    round(float(self.extent) / self.full_extent * 100))
            self.canvas.itemconfigure(self.label_id, text=percent)
        if(percent == '100%'):
            self.toggle_pause()
        self.canvas.after(self.interval, self.step, delta)


    def toggle_pause(self):
        self.running = not self.running

root = tk.Tk()
app = Application(master=root)
# Start the event loop
app.mainloop()