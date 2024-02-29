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


def main():
    drive_ctrl = DriveManager()

    #Home
    print("---HOMING---")
    asyncio.run(CPRmotorctrl.home(drive_ctrl))
    print("---DONE HOMING---")

    #Create a new folder for were photos will go
    print("starting image cycling")
    imagesforProcessingFolder = "baseplatePhotos"
    os.makedirs(imagesforProcessingFolder)

     #Manually addnig photos for test
    shutil.copy(os.path.join('image1.jpg'), os.path.join(imagesforProcessingFolder, 'image1.jpg'))
    shutil.copy(os.path.join('image2.jpg'), os.path.join(imagesforProcessingFolder, 'image2.jpg'))
    shutil.copy(os.path.join('image3.jpg'), os.path.join(imagesforProcessingFolder, 'image3.jpg'))
    shutil.copy(os.path.join('image4.jpg'), os.path.join(imagesforProcessingFolder, 'image4.jpg'))
    shutil.copy(os.path.join('image5.jpg'), os.path.join(imagesforProcessingFolder, 'image5.jpg'))
    shutil.copy(os.path.join('image6.jpg'), os.path.join(imagesforProcessingFolder, 'image6.jpg'))
    
    #Take Images of Petri Dishes and adds to new fodler
    tempFolder = "tempPhotos"
    os.makedirs(tempFolder)
    numPetriDishes = 6  #TODO this should come from GUI
    asyncio.run(CPRmotorctrl.takePhotos(tempFolder, numPetriDishes, drive_ctrl))    #TODO will need to incorporate motor controls

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
    
    #GO toeach colony, deposit, steralize needle
    dwell_duration = 5 # TODO input from GUI
    asyncio.run(CPRmotorctrl.executeToolPath(coloniesToSample, dwell_duration, drive_ctrl))

    #call image meta data with the file created above
    cpr.create_metadata(image_folder_path=imagesforProcessingFolder, colony_coords_folder_path='./sampleColonies', create_petri_dish_view=True, create_colony_view= True)

    #currently deleting the file after execution- will need to delete end of program
    shutil.rmtree('goodColonies')  
    shutil.rmtree(imagesforProcessingFolder)
    shutil.rmtree('runs')
    shutil.rmtree('sampleColonies')
    shutil.rmtree('yolo_dump')
    
main()