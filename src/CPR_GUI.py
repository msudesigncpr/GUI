import tkinter as tk
from tkinter import ttk
import cv2 as cv
import openpyxl
import numpy as np
import time
from tkinter import messagebox

#GUI variables
LARGEFONT = ("Elephant", 36)
smallFont = ("calibri", 12)
numPetriDishes = 1

#App-------------------------------------------------------------------------------------------
class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #set up screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f'{screen_width}x{screen_height}')  # Set the size of the window to fill the screen
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        #for F in (UserInputs):
        frame = UserInputs(container, self)
        self.frames[UserInputs] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(UserInputs)

        # Bind the closing event to the on_closing function
        self.protocol("WM_DELETE_WINDOW", self.onClosing)
    
    #allows the screen to play
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    def returnValues(self):
        user_input_frame = self.frames[UserInputs]
        return user_input_frame.getRunName(), user_input_frame.getNames(), user_input_frame.getDwellTime(), user_input_frame.getPetris()
    
    def saveInputs(self):
        runName, names, dwell_duration, petri_dish_count = self.returnValues()

    def onPause(self):
        stop = 1
        return stop

    def onStart(self):
        start = 1
        return start

    def onClosing(self):
        self.destroy()  # Properly close the application    

#Page to input user paramaters
class UserInputs(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.names = []

        #label for what to do on this page
        label = ttk.Label(self, text="Input Data Options", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        #user can input data set name and access this name
        dataName = tk.Label(self, text="Please give this data set a name ", font=smallFont)
        dataName.grid(row=1, column=1)
        self.nameVar = tk.StringVar()
        nameEntry = tk.Entry(self, textvariable = self.nameVar, font = smallFont)
        nameEntry.grid(row=1, column=2)

        #user can input dwell time
        dataDwell = tk.Label(self, text="How long would you like the dwell time to be? ", font=smallFont)
        dataDwell.grid(row=2, column=1)
        self.dwellVar = tk.StringVar()
        dwellEntry = tk.Entry(self, textvariable = self.dwellVar, font = smallFont)
        dwellEntry.grid(row=2, column=2)

        #user can input how many Petri dishes in this eperiment
        dataPetris = tk.Label(self, text="How many Petri dishes did you place? ", font=smallFont)
        dataPetris.grid(row=3, column=1)
        self.petrisVar = tk.StringVar()
        numPetris = tk.Entry(self, textvariable = self.petrisVar, font = smallFont)
        numPetris.grid(row=3, column=2)

        return_button = tk.Button(self, text="Accept Inputs", command=controller.saveInputs)
        return_button.grid(row=15, column=2)

        #send a pop-up message to user asking if they inputed data correctly
        result = tk.Label(self, text="", font=smallFont)
        result.grid(row=4, column=2)
        confirm = ttk.Button(self, text="Check Inputs", command=lambda: self.verifyInput())
        confirm.grid(row=4, column=2)

        '''
        close_button = tk.Button(self, text="STOP", command=controller.onPause,font=("Helvetica", 16, "bold"), fg="red")
        close_button.grid(row=20, column=1)

        start_button = tk.Button(self, text="START", command=controller.onStart, font=("Helvetica", 16, "bold"), fg="green")
        start_button.grid(row=20, column=2)
        '''
        quit_button = tk.Button(self, text="Quit", command=controller.onClosing, font=smallFont)
        quit_button.grid(row=30, column=1)
                

    #allows to access dwell times, petris and name elsewhere
    def getRunName(self):
        return self.nameVar.get()
    def getDwellTime(self):
        dwellTime = self.dwellVar.get()
        return int(dwellTime)
    def getPetris(self):
        petris = self.petrisVar.get()
        if petris.isdigit():
            return int(petris)
        else:
            return 0
    def getNames(self):
            return self.names
    
    #once button is pressed it will add workbook pages and save given name
    def verifyInput(self):
        p = self.petrisVar.get()
        messagebox.showinfo("STATUS", "VERIFY YOUR PETRI DISHES & WELL PLATE ARE PLACED HOW THEY SHOULD BE")

        for i in range(int(self.getPetris())):
                label_text = f"What is the name of Petri dish {i + 1}? "
                petris_label = tk.Label(self, text=label_text, font=smallFont)
                petris_label.grid(row=5 + i, column=1)

                petris_var = tk.StringVar()
                name = tk.Entry(self, textvariable=petris_var, font=smallFont)
                name.grid(row=5 + i, column=2)

                save = ttk.Button(self, text="Enter", command=lambda entry=name, index=i: self.setName(entry, index, self.names))
            
                save.grid(row=5 + i, column=3)

        return self.names

    def setName(self, entry, i, names):
        name = entry.get()
        petris_label = tk.Label(self, text=name, font=smallFont)
        petris_label.grid(row=5 + i, column=2)

        names.append(name)

        entry.grid_forget() 