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
import time
from dataclasses import dataclass
import CPR_tools as cpr
import CPR_random
import CPRmotorctrl
import asyncio
from libmotorctrl import DriveManager, DriveTarget
#import pages

imagesforProcessingFolder = "baseplatePhotos"


def main():
    tmp_directories = ['goodColonies', imagesforProcessingFolder, 'pinHolePhoto', 'runs', 'sampleColonies', 'yolo_dump', 'metadata']
    for dir in tmp_directories:
        if os.path.exists(dir) and os.path.isdir(dir):
            logging.warning("Deleting leftover tmp directory %s (did the last run finish successfully?)", dir)
            shutil.rmtree(dir)

    drive_ctrl = DriveManager()

    #Home
    print("---HOMING---")
    asyncio.run(CPRmotorctrl.home(drive_ctrl))
    print("---DONE HOMING---")

    #Manually set calibration
    CPRmotorctrl.calibrate(drive_ctrl, 15560, 125940)

    #Image pinhole
    print("Starting pinhole cycle")
    pinHole = "pinHolePhoto"
    os.makedirs(pinHole)
    asyncio.run(CPRmotorctrl.pinhole(drive_ctrl, pinHole))  #TODO change this out of the temp folder to pinhole folder
    #offsetX, offsetY = cpr.pinhole('./pinHolePhoto/pinhole.jpg', save_image_path= './pinHolePhoto/pinhole.jpg', row_deviation_threshold=.1, column_deviation_threshold=.1, center_point=(0.5, 0.48))
    print("applying offset")  #TODO setcalibration offset

    #Create a new folder for were photos will go
    print("starting image cycling")
    os.makedirs(imagesforProcessingFolder)
    numPetriDishes = 6  #TODO this should come from GUI
    asyncio.run(CPRmotorctrl.takePhotos(imagesforProcessingFolder, numPetriDishes, drive_ctrl))

    #create a folder where text files of good corddinates will be placed
    goodColoniesFolder = "goodColonies"
    os.makedirs(goodColoniesFolder)
    cpr.process_petri_dish_image(image_folder_path=imagesforProcessingFolder, good_colony_coord_output_path=goodColoniesFolder)
   
    #Randomize and select 96 colonies using images from new folder *produces sampledColoniesFolder
    coloniesToSample =CPR_random.randomize(goodColoniesFolder)   
    
    #call image meta data with the file created above
    cpr.create_metadata(image_folder_path=imagesforProcessingFolder, colony_coords_folder_path='./sampleColonies', create_petri_dish_view=True, create_colony_view= True)

    #GO toeach colony, deposit, steralize needle
    dwell_duration = 5 # TODO input from GUI
    asyncio.run(CPRmotorctrl.executeToolPath(coloniesToSample, dwell_duration, drive_ctrl))
    
    #currently deleting the file after execution- will need to delete end of program
    shutil.rmtree('goodColonies')  
    shutil.rmtree(imagesforProcessingFolder)
    shutil.rmtree('runs')
    shutil.rmtree('sampleColonies')
    shutil.rmtree('yolo_dump')
    
    
main()
