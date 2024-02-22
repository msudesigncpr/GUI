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
import sys
import time
from dataclasses import dataclass
from libmotorctrl import DriveOverseer, DriveTarget
import CPR_tools as cpr
import datetime
import CPR_random

LOGLEVEL = logging.INFO

STERILIZER_COORDINATES = (461_330, 87_950, 60_000)  # Micrometers  # TODO
PETRI_DISH_DEPTH = 80_000  # Micrometers # TODO Check depth
WELL_DEPTH = 80_000  # Micrometers # TODO Check depth

logging.basicConfig(
    format="%(asctime)s: %(threadName)s: %(message)s",
    level=LOGLEVEL,
    datefmt="%H:%M:%S",
)


@dataclass
class Well:
    id: str
    x: float
    y: float
    has_sample: bool
    origin: str


@dataclass
class Colony:
    dish: str
    x: float
    y: float


WELLS = [
    Well(id="A1", x=267.79, y=31.08, has_sample=False, origin=None),
    Well(id="A2", x=276.86, y=31.08, has_sample=False, origin=None),
    Well(id="A3", x=285.93, y=31.08, has_sample=False, origin=None),
    Well(id="A4", x=295.00, y=31.08, has_sample=False, origin=None),
    Well(id="A5", x=304.07, y=31.08, has_sample=False, origin=None),
    Well(id="A6", x=313.14, y=31.08, has_sample=False, origin=None),
    Well(id="A7", x=322.21, y=31.08, has_sample=False, origin=None),
    Well(id="A8", x=331.28, y=31.08, has_sample=False, origin=None),
    Well(id="A9", x=340.35, y=31.08, has_sample=False, origin=None),
    Well(id="A10", x=349.42, y=31.08, has_sample=False, origin=None),
    Well(id="A11", x=358.49, y=31.08, has_sample=False, origin=None),
    Well(id="A12", x=367.56, y=31.08, has_sample=False, origin=None),
    Well(id="B1", x=267.79, y=40.15, has_sample=False, origin=None),
    Well(id="B2", x=276.86, y=40.15, has_sample=False, origin=None),
    Well(id="B3", x=285.93, y=40.15, has_sample=False, origin=None),
    Well(id="B4", x=295.00, y=40.15, has_sample=False, origin=None),
    Well(id="B5", x=304.07, y=40.15, has_sample=False, origin=None),
    Well(id="B6", x=313.14, y=40.15, has_sample=False, origin=None),
    Well(id="B7", x=322.21, y=40.15, has_sample=False, origin=None),
    Well(id="B8", x=331.28, y=40.15, has_sample=False, origin=None),
    Well(id="B9", x=340.35, y=40.15, has_sample=False, origin=None),
    Well(id="B10", x=349.42, y=40.15, has_sample=False, origin=None),
    Well(id="B11", x=358.49, y=40.15, has_sample=False, origin=None),
    Well(id="B12", x=367.56, y=40.15, has_sample=False, origin=None),
    Well(id="C1", x=267.79, y=49.22, has_sample=False, origin=None),
    Well(id="C2", x=276.86, y=49.22, has_sample=False, origin=None),
    Well(id="C3", x=285.93, y=49.22, has_sample=False, origin=None),
    Well(id="C4", x=295.00, y=49.22, has_sample=False, origin=None),
    Well(id="C5", x=304.07, y=49.22, has_sample=False, origin=None),
    Well(id="C6", x=313.14, y=49.22, has_sample=False, origin=None),
    Well(id="C7", x=322.21, y=49.22, has_sample=False, origin=None),
    Well(id="C8", x=331.28, y=49.22, has_sample=False, origin=None),
    Well(id="C9", x=340.35, y=49.22, has_sample=False, origin=None),
    Well(id="C10", x=349.42, y=49.22, has_sample=False, origin=None),
    Well(id="C11", x=358.49, y=49.22, has_sample=False, origin=None),
    Well(id="C12", x=367.56, y=49.22, has_sample=False, origin=None),
    Well(id="D1", x=267.79, y=58.29, has_sample=False, origin=None),
    Well(id="D2", x=276.86, y=58.29, has_sample=False, origin=None),
    Well(id="D3", x=285.93, y=58.29, has_sample=False, origin=None),
    Well(id="D4", x=295.00, y=58.29, has_sample=False, origin=None),
    Well(id="D5", x=304.07, y=58.29, has_sample=False, origin=None),
    Well(id="D6", x=313.14, y=58.29, has_sample=False, origin=None),
    Well(id="D7", x=322.21, y=58.29, has_sample=False, origin=None),
    Well(id="D8", x=331.28, y=58.29, has_sample=False, origin=None),
    Well(id="D9", x=340.35, y=58.29, has_sample=False, origin=None),
    Well(id="D10", x=349.42, y=58.29, has_sample=False, origin=None),
    Well(id="D11", x=358.49, y=58.29, has_sample=False, origin=None),
    Well(id="D12", x=367.56, y=58.29, has_sample=False, origin=None),
    Well(id="E1", x=267.79, y=67.36, has_sample=False, origin=None),
    Well(id="E2", x=276.86, y=67.36, has_sample=False, origin=None),
    Well(id="E3", x=285.93, y=67.36, has_sample=False, origin=None),
    Well(id="E4", x=295.00, y=67.36, has_sample=False, origin=None),
    Well(id="E5", x=304.07, y=67.36, has_sample=False, origin=None),
    Well(id="E6", x=313.14, y=67.36, has_sample=False, origin=None),
    Well(id="E7", x=322.21, y=67.36, has_sample=False, origin=None),
    Well(id="E8", x=331.28, y=67.36, has_sample=False, origin=None),
    Well(id="E9", x=340.35, y=67.36, has_sample=False, origin=None),
    Well(id="E10", x=349.42, y=67.36, has_sample=False, origin=None),
    Well(id="E11", x=358.49, y=67.36, has_sample=False, origin=None),
    Well(id="E12", x=367.56, y=67.36, has_sample=False, origin=None),
    Well(id="F1", x=267.79, y=76.43, has_sample=False, origin=None),
    Well(id="F2", x=276.86, y=76.43, has_sample=False, origin=None),
    Well(id="F3", x=285.93, y=76.43, has_sample=False, origin=None),
    Well(id="F4", x=295.00, y=76.43, has_sample=False, origin=None),
    Well(id="F5", x=304.07, y=76.43, has_sample=False, origin=None),
    Well(id="F6", x=313.14, y=76.43, has_sample=False, origin=None),
    Well(id="F7", x=322.21, y=76.43, has_sample=False, origin=None),
    Well(id="F8", x=331.28, y=76.43, has_sample=False, origin=None),
    Well(id="F9", x=340.35, y=76.43, has_sample=False, origin=None),
    Well(id="F10", x=349.42, y=76.43, has_sample=False, origin=None),
    Well(id="F11", x=358.49, y=76.43, has_sample=False, origin=None),
    Well(id="F12", x=367.56, y=76.43, has_sample=False, origin=None),
    Well(id="G1", x=267.79, y=85.5, has_sample=False, origin=None),
    Well(id="G2", x=276.86, y=85.5, has_sample=False, origin=None),
    Well(id="G3", x=285.93, y=85.5, has_sample=False, origin=None),
    Well(id="G4", x=295.00, y=85.5, has_sample=False, origin=None),
    Well(id="G5", x=304.07, y=85.5, has_sample=False, origin=None),
    Well(id="G6", x=313.14, y=85.5, has_sample=False, origin=None),
    Well(id="G7", x=322.21, y=85.5, has_sample=False, origin=None),
    Well(id="G8", x=331.28, y=85.5, has_sample=False, origin=None),
    Well(id="G9", x=340.35, y=85.5, has_sample=False, origin=None),
    Well(id="G10", x=349.42, y=85.5, has_sample=False, origin=None),
    Well(id="G11", x=358.49, y=85.5, has_sample=False, origin=None),
    Well(id="G12", x=367.56, y=85.5, has_sample=False, origin=None),
    Well(id="H1", x=267.79, y=94.57, has_sample=False, origin=None),
    Well(id="H2", x=276.86, y=94.57, has_sample=False, origin=None),
    Well(id="H3", x=285.93, y=94.57, has_sample=False, origin=None),
    Well(id="H4", x=295.00, y=94.57, has_sample=False, origin=None),
    Well(id="H5", x=304.07, y=94.57, has_sample=False, origin=None),
    Well(id="H6", x=313.14, y=94.57, has_sample=False, origin=None),
    Well(id="H7", x=322.21, y=94.57, has_sample=False, origin=None),
    Well(id="H8", x=331.28, y=94.57, has_sample=False, origin=None),
    Well(id="H9", x=340.35, y=94.57, has_sample=False, origin=None),
    Well(id="H10", x=349.42, y=94.57, has_sample=False, origin=None),
    Well(id="H11", x=358.49, y=94.57, has_sample=False, origin=None),
    Well(id="H12", x=367.56, y=94.57, has_sample=False, origin=None),
]

#Set up the camera
cam_port = 0
cam = cv.VideoCapture(cam_port, cv.CAP_DSHOW)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 3264)          #set frame width (max res from data sheet)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 2558)          #set frame heigh (max res from data sheet)


#Takes photos x amount of petri dishes (user specified) and saves to new folder
def takePhotos(folder_path, numPetriDishes):
    petriLocations = [[66.11, 62.57], [66.11, -58.08], [180.41, 62.57], 
                      [180.41, -58.08], [294.71, 62.57], [409.01, 62.57]]
    petriCounter = 0
    for i in range(1, numPetriDishes + 1):
        #move to petriLocations[petriCounter]
        result, image = cam.read()
        print("----------IMAGE TAKEN----------")
        if result:
            imgName = f"petri_dish_{i}.jpg"
            cv.imwrite(imgName, image)
            img_path_to_save = os.path.join(folder_path, imgName)
            shutil.move(imgName, img_path_to_save)
        petriCounter = petriCounter + 1
    cam.release()

def executeToolPath(raw_colony_list, dwell_duration):
    dwell_duration = 5

    logging.info("Initializing drives...")

    drive_ctrl = DriveOverseer()
    drive_ctrl.home(DriveTarget.DriveZ)
    drive_ctrl.home(DriveTarget.DriveX)
    drive_ctrl.home(DriveTarget.DriveY)

    # drive_ctrl.calibrate()

    # TODO Error propagation

    target_colonies = []
    for colony in raw_colony_list:
        target_colonies.append(Colony(dish="P0", x=colony[0], y=colony[1]))

    logging.info("Target colonies list acquired!")

    logging.info("Performing initial sterilization...")
    drive_ctrl.move(
        STERILIZER_COORDINATES[0],
        STERILIZER_COORDINATES[1],
        STERILIZER_COORDINATES[2],
    )
    logging.info(f"Sleeping for {dwell_duration} seconds...")
    time.sleep(dwell_duration)

    for colony in target_colonies:
        logging.info("Starting sampling cycle...")
        logging.info(
            f"Target colony is at {colony.x:.2f}, {colony.y:.2f} in Petri dish {colony.dish}"
        )
        # TODO Remove code below when well_target known
        well_target = None
        for well_candidate in WELLS:
            if not well_candidate.has_sample:
                well_target = well_candidate
                logging.info(f"Target well is {well_target.id}")
                break
        if well_target is None:
            logging.error("No unused wells!")  # TODO Handle differently
            sys.exit(1)
        
        drive_ctrl.move(
            int(colony.x * 10**3), int(colony.y * 10**3), PETRI_DISH_DEPTH
        )
        logging.info("Colony collected, moving to well...")
        drive_ctrl.move(
            int(well_target.x * 10**3), int(well_target.y * 10**3), WELL_DEPTH
        )
        logging.info("Well reached, moving to sterilizer...")
        well_target.has_sample = True
        well_target.origin = colony.dish
        drive_ctrl.move(
            STERILIZER_COORDINATES[0],
            STERILIZER_COORDINATES[1],
            STERILIZER_COORDINATES[2],
        )
        logging.info(f"Sleeping for {dwell_duration} seconds...")
        time.sleep(dwell_duration)

    logging.info("Sampling complete!")
    drive_ctrl.move(490_000, -90_000, 0)
    drive_ctrl.terminate()

def main():     
    #Create a new folder for were photos will go
    imagesforProcessingFolder = "baseplatePhotos"
    os.makedirs(imagesforProcessingFolder)

     #Manually addnig photos for test
    shutil.copy(os.path.join('petri_dish_1.jpg'), os.path.join(imagesforProcessingFolder, 'image1.jpg'))
    shutil.copy(os.path.join('petri_dish_2.jpg'), os.path.join(imagesforProcessingFolder, 'image2.jpg'))
    shutil.copy(os.path.join('petri_dish_3.jpg'), os.path.join(imagesforProcessingFolder, 'image3.jpg'))
    shutil.copy(os.path.join('petri_dish_4.jpg'), os.path.join(imagesforProcessingFolder, 'image4.jpg'))
    shutil.copy(os.path.join('petri_dish_5.jpg'), os.path.join(imagesforProcessingFolder, 'image5.jpg'))
    shutil.copy(os.path.join('petri_dish_6.jpg'), os.path.join(imagesforProcessingFolder, 'image6.jpg'))

    '''
    #Take Images of Petri Dishes and adds to new fodler
    numPetriDishes = 6  #TODO this should come from GUI
    takePhotos(photosFolder, numPetriDishes)    #TODO will need to incorporate motor controls***
    '''

    #create a folder where text files of good corddinates will be placed
    goodColoniesFolder = "goodColonies"
    os.makedirs(goodColoniesFolder)

    #create a folder where all corddinates will be placed
    #allColoniesFolder = "allColonies"
    #os.makedirs(allColoniesFolder)

    #call image processing using the folder created
    #cpr.process_petri_dish_image(image_folder_path=imagesforProcessingFolder, good_colony_coord_output_path=goodColoniesFolder)
    #Manually addnig text files for test
    shutil.copy(os.path.join('example1.txt'), os.path.join(goodColoniesFolder, 'example1.txt'))
    shutil.copy(os.path.join('example2.txt'), os.path.join(goodColoniesFolder, 'example2.txt'))
    shutil.copy(os.path.join('example3.txt'), os.path.join(goodColoniesFolder, 'example3.txt'))
    shutil.copy(os.path.join('example4.txt'), os.path.join(goodColoniesFolder, 'example4.txt'))
    shutil.copy(os.path.join('example5.txt'), os.path.join(goodColoniesFolder, 'example5.txt'))
    shutil.copy(os.path.join('example6.txt'), os.path.join(goodColoniesFolder, 'example6.txt'))


    #Randomize and select 96 colonies using images from new folder
    coloniesToSample =CPR_random.randomize(goodColoniesFolder)   
    
    #GO toeach colony, deposit, steralize needle
    dwell_duration = 5 # TODO input from GUI
    #executeToolPath(coloniesToSample, dwell_duration)

    #call image meta data with the file created above
    cpr.create_metadata(imagesforProcessingFolder='./images/', goodColoniesFolder='./good_colony_coords/', create_petri_dish_view=True, create_colony_view= True)

    #currently deleting the file after execution- will need to delete end of program
    #shutil.rmtree(sampledColoniesFolder)  
    shutil.rmtree(imagesforProcessingFolder)
    #shutil.rmtree(photosFolder)
    
main()