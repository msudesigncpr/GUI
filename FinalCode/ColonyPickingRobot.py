import random
import os, glob
import shutil
from msilib.schema import _Validation_records
import cv2 as cv
import numpy as np
import openpyxl
import time
import threading
import json
import csv
import logging
import CPR_random
import CPR_tools as cpr
'''
import time
from dataclasses import dataclass
import CPR_tools as cpr
import CPR_random
import CPRmotorctrl
import asyncio
from libmotorctrl import DriveManager, DriveTarget
'''
import tkinter as tk
from tkinter import ttk
import pages

def main():
    #Start GUI

    
    app = pages.tkinterApp()
    #names, dwell, num = app.mainloop()
    app.mainloop()
    runName, names, dwell, num = app.returnValues()
    print(runName, names, dwell, num)
    

    #TODO delete temp folder when all running
    tempFolder = "tempPhotos"
    os.makedirs(tempFolder)

    '''
    #Home and setup drive manager
    drive_ctrl = DriveManager()
    print("---HOMING---")
    asyncio.run(CPRmotorctrl.home(drive_ctrl))
    print("---DONE HOMING---")
    

    #Image pinhole
    print("Starting pinhole cycle")
    pinHole = "pinHolePhoto"
    os.makedirs(pinHole)
    shutil.copy(os.path.join('pinhole.jpg'), os.path.join(pinHole, 'pinhole.jpg'))  #TODO delte this after running with real photo
    asyncio.run(CPRmotorctrl.pinhole(drive_ctrl, tempFolder))  #TODO change this out of the temp folder to pinhole folder
    diviation = cpr.pinhole('./pinHolePhoto/pinhole.jpg', save_image_path= './pinHolePhoto/pinhole.jpg', row_deviation_threshold=.1, column_deviation_threshold=.1, center_point=(0.5, 0.48))
    if(diviation[0] != 1 and diviation[1] != 1):
        offsetX = diviation[0]
        offsetY = diviation[1]
        print("applying offset")
        #TODO setcalibration offset
'''
    #Create a new folder for were photos will go
    print("starting image cycling")
    imagesforProcessingFolder = "baseplatePhotos"
    os.makedirs(imagesforProcessingFolder)
    #TODO delte when no longer using test images
    shutil.copy(os.path.join('image1.jpg'), os.path.join(imagesforProcessingFolder, 'image1.jpg'))
    shutil.copy(os.path.join('image2.jpg'), os.path.join(imagesforProcessingFolder, 'image2.jpg'))
    shutil.copy(os.path.join('image3.jpg'), os.path.join(imagesforProcessingFolder, 'image3.jpg'))
    shutil.copy(os.path.join('image4.jpg'), os.path.join(imagesforProcessingFolder, 'image4.jpg'))
    shutil.copy(os.path.join('image5.jpg'), os.path.join(imagesforProcessingFolder, 'image5.jpg'))
    shutil.copy(os.path.join('image6.jpg'), os.path.join(imagesforProcessingFolder, 'image6.jpg'))
    
    '''
    #Take Images of Petri Dishes and adds to new fodler
    numPetriDishes = 6  #TODO this should come from GUI
    asyncio.run(CPRmotorctrl.takePhotos(tempFolder, numPetriDishes, drive_ctrl))    #TODO will need to change tempFOlder to
    '''
    #create a folder where text files of good corddinates will be placed
    goodColoniesFolder = "goodColonies"
    os.makedirs(goodColoniesFolder)

    #create a folder where all corddinates will be placed
    #allColoniesFolder = "allColonies"
    #os.makedirs(allColoniesFolder)

    #call image processing using the folder created
    cpr.process_petri_dish_image(image_folder_path=imagesforProcessingFolder, good_colony_coord_output_path=goodColoniesFolder)
   
    #Randomize and select 96 colonies using images from new folder *produces sampledColoniesFolder
    coloniesToSample =CPR_random.randomize(goodColoniesFolder)   
    
    #call image meta data with the file created above
    cpr.create_metadata(image_folder_path=imagesforProcessingFolder, colony_coords_folder_path='./sampleColonies', create_petri_dish_view=True, create_colony_view= True)

    '''
    #GO toeach colony, deposit, steralize needle
    dwell_duration = 5 # TODO input from GUI
    asyncio.run(CPRmotorctrl.executeToolPath(coloniesToSample, dwell_duration, drive_ctrl))
    '''
    
    #currently deleting the file after execution- will need to delete end of program
    shutil.rmtree('goodColonies')  
    shutil.rmtree(imagesforProcessingFolder)
    shutil.rmtree('runs')
    shutil.rmtree('sampleColonies')
    shutil.rmtree('yolo_dump')
    
    
main()