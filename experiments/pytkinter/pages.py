import tkinter as tk
from tkinter import ttk
import cv2 as cv
import openpyxl
import numpy as np
import time
from tkinter import messagebox

# GUI variables
LARGEFONT = ("Elephant", 36)
smallFont = ("calibri", 12)
numPetriDishes = 1

# Excel-----------------------------------------------------------------------------------------
workbook = openpyxl.Workbook()
worksheet = workbook.active
worksheet.title = "Intro"
worksheet["A1"] = "Each page is for a new Petri Dish"
# ----------------------------------------------------------------------------------------------

# Camera----------------------------------------------------------------------------------------
cam_port = 0
cam = cv.VideoCapture(cam_port, cv.CAP_DSHOW)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 3264)  # set frame width (max res from data sheet)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 2558)  # set frame heigh (max res from data sheet)
# Un-distort, arrays came from calibarate funtions in calibrate.py file
DIM = (3264, 2448)
K = np.array(
    [
        [441830.0440255356, 0.0, 852.1256225236111],
        [0.0, 516414.51234938996, 1245.8722842811067],
        [0.0, 0.0, 1.0],
    ]
)
D = np.array(
    [
        [-882.310014580582],
        [590380.1877261768],
        [231827527.76974776],
        [-2385332774656.0986],
    ]
)
# ----------------------------------------------------------------------------------------------


# App-------------------------------------------------------------------------------------------
class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # set up screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(
            f"{screen_width}x{screen_height}"
        )  # Set the size of the window to fill the screen
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        # calls all of the possible screens
        for F in (StartPage, Page1, Page2, Steps):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    # allows the screen to play
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    # can print any words- testing purposes
    def printWords(self):
        print("Your submission is being processed")

    # used in the pop up window in Page1
    def data_button(self, petris):
        # message= f"ARE THE PETRI DISHED ORIENTED CORRECTLY \n & \n DO YOU HAVE {petris} PETRI DISHES PLACED 1 THROUGH {petris}"
        messagebox.showinfo(
            "STATUS",
            f"ARE THE PETRI DISHED ORIENTED CORRECTLY \n & \n DO YOU HAVE {petris} PETRI DISHES PLACED 1 THROUGH {petris}",
        )

    # creates a certain amount of excel pages based on user input
    def excelPages(self, petris):
        global numPetriDishes
        numPetris = int(petris)
        numPetriDishes = numPetris
        for i in range(1, numPetris + 1):
            sheetName = f"Petridish{i}"
            workbook.create_sheet(title=sheetName)

    # def saveNumPetris(self, petris):
    #    numPetris = int(petris)
    #    global numPetriDishes
    #    numPetriDishes = numPetris

    def getNumPetris(self):
        global numPetriDishes
        return numPetriDishes

    def addImage(self, i):
        title = f"Petridish{i}"
        worksheet = workbook.title
        worksheet["A1"] = "Petri Dish 1"
        img = f"PetriDish{i}.img"
        img.anchor = "A2"
        worksheet.add_image(img)

    # saves the excel workbook given user's name- should be called last
    def save_excel(self, name):
        print("hello" + name)
        name = name + ".xlsx"
        workbook.save(name)

    # Takes an image and saves it to the working file labeled with the time
    def takePhoto(self):
        i = 1
        result, image = cam.read()
        if result:
            imgName = f"PetriDish{i}.jpg"
            cv.imwrite(imgName, image)
            i = i + 1

        else:
            print("No image detected")
            # return None

    # undistort the image
    def undistort(img_path):
        img = cv.imread(img_path)
        h, w = img.shape[:2]
        map1, map2 = cv.fisheye.initUndistortRectifyMap(
            K, D, np.eye(3), K, DIM, cv.CV_16SC2
        )
        undistorted_img = cv.remap(
            img,
            map1,
            map2,
            interpolation=cv.INTER_LINEAR,
            borderMode=cv.BORDER_CONSTANT,
        )

        return undistorted_img


# This is the intro page and user can go to 2 options- calibarate camera or start test
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # label for current page
        label = ttk.Label(self, text="Startpage", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # Buttons to go to other pages
        page1 = ttk.Button(
            self,
            text="Input Data Options",
            command=lambda: controller.show_frame(Page1),
        )
        page1.grid(row=2, column=1, padx=10, pady=10)
        page2 = ttk.Button(
            self, text="Calibarate Camera", command=lambda: controller.show_frame(Page2)
        )
        page2.grid(row=3, column=1, padx=10, pady=10)

        # label for what to do on this page
        hello = ttk.Label(
            self,
            text="Welcome to the colony picking robot, please select a following option",
            font=smallFont,
        )
        hello.grid(row=1, column=1, padx=10, pady=10)


# Page to input user paramaters
class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # label for what to do on this page
        label = ttk.Label(self, text="Input Data Options", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # user can input data set name and access this name
        dataName = tk.Label(
            self, text="Please give this data set a name ", font=smallFont
        )
        dataName.grid(row=1, column=1)
        self.nameVar = tk.StringVar()
        nameEntry = tk.Entry(self, textvariable=self.nameVar, font=smallFont)
        nameEntry.grid(row=1, column=2)
        # controller.save_excel(self.getName())

        # user can input dwell time
        dataDwell = tk.Label(
            self, text="How long would you like the dwell time to be? ", font=smallFont
        )
        dataDwell.grid(row=2, column=1)
        self.dwellVar = tk.StringVar()
        dwellEntry = tk.Entry(self, textvariable=self.dwellVar, font=smallFont)
        dwellEntry.grid(row=2, column=2)

        # user can input how many Petri dishes in this eperiment
        dataPetris = tk.Label(
            self, text="How many Petri dishes did you place? ", font=smallFont
        )
        dataPetris.grid(row=3, column=1)
        self.petrisVar = tk.StringVar()
        numPetris = tk.Entry(self, textvariable=self.petrisVar, font=smallFont)
        numPetris.grid(row=3, column=2)

        # global numPetriDishes
        # numPetriDishes = int(numPetris)
        # controller.saveNumPetris(numPetris)

        # send a pop-up message to user asking if they inputed data correctly
        result = tk.Label(self, text="", font=smallFont)
        result.grid(row=9, column=2)
        button = ttk.Button(
            self, text="Input data", command=lambda: self.dataInput(controller)
        )
        button.grid(row=9, column=2)

        # buttons to other pages
        moveOn = ttk.Button(
            self, text="Continue", command=lambda: controller.show_frame(Steps)
        )
        moveOn.grid(row=10, column=2, padx=10, pady=10)
        start = ttk.Button(
            self, text="StartPage", command=lambda: controller.show_frame(StartPage)
        )
        start.grid(row=11, column=2, padx=10, pady=10)
        page2 = ttk.Button(
            self, text="Calibarate Camera", command=lambda: controller.show_frame(Page2)
        )
        page2.grid(row=11, column=3, padx=10, pady=10)

    # allows to access dwell times, petris and name elsewhere
    def getDwellTime(self):
        return self.dwellVar.get()

    def getPetris(self):
        return self.petrisVar.get()

    def getName(self):
        return self.nameVar.get()

    # once button is pressed it will add workbook pages and save given name
    def dataInput(self, controller):
        name = self.getName()
        petris = self.getPetris()
        controller.excelPages(petris)
        controller.saveNumPetris(petris)
        controller.save_excel(name)
        messagebox.showinfo(
            "STATUS",
            f"ARE THE PETRI DISHES ORIENTED CORRECTLY \n & \n DO YOU HAVE {self.getPetris()} PETRI DISHES PLACED 1 THROUGH {self.getPetris()}",
        )


# currently lists the steps being taken
class Steps(tk.Frame):
    def __init__(self, parent, controller):  # page1_instance
        tk.Frame.__init__(self, parent)

        # i = num_petri_dishes
        # for i in range(1, numPetriDishes + 1):
        # user can input the names of the Petri dishes
        i = "1"
        petrisName = tk.Label(
            self, text=f"Insert name of Petri dish{i}", font=smallFont
        )
        petrisName.grid(row=2, column=1)
        self.petrisVar = tk.StringVar()
        petrisEntry = tk.Entry(self, textvariable=self.petrisVar, font=smallFont)
        petrisEntry.grid(row=2, column=2)

        # petris = controller.getNumPetris()
        global numPetriDishes
        petris = numPetriDishes
        # loop this depending on what the number of petri dishes are
        # lISTING WHAT THE NEXT STEPS ARE
        dataName = tk.Label(self, text=f"{petris}", font=smallFont)
        dataName.grid(row=4, column=4)
        dataName = tk.Label(self, text="Locating Petri Dish 1 ", font=smallFont)
        dataName.grid(row=5, column=4)
        dataName = tk.Label(
            self, text="Taking Picture ", font=smallFont
        )  # take pic after checking if at the right location
        dataName.grid(row=6, column=4)
        dataName = tk.Label(self, text="Locating Colonies ", font=smallFont)
        dataName.grid(row=7, column=4)

        # Brings back to homewcreen
        button2 = ttk.Button(
            self, text="QUIT", command=lambda: controller.show_frame(StartPage)
        )
        button2.grid(row=20, column=1, padx=10, pady=10)


# calibarating page- currently takes an image when commanded
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # page title
        label = ttk.Label(self, text="Calibarate Camera", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # Takes the photo- and saves photo to file
        button = ttk.Button(
            self, text="Take an Image", command=lambda: controller.takePhoto()
        )  # may need to remove () at end
        button.grid(row=1, column=4, padx=10, pady=10)

        # record the location it is at and check with expected location

        # buttons to other pages
        page1 = ttk.Button(
            self,
            text="Input Data Options",
            command=lambda: controller.show_frame(Page1),
        )
        page1.grid(row=20, column=1, padx=10, pady=10)
        start = ttk.Button(
            self, text="Startpage", command=lambda: controller.show_frame(StartPage)
        )
        start.grid(row=20, column=2, padx=10, pady=10)


app = tkinterApp()
app.mainloop()
