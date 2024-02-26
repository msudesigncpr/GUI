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
#from dataclasses import dataclass
#from libmotorctrl import DriveOverseer, DriveTarget
#from constants import *
import CPR_tools as cpr
import CPR_random
#import CPRmotorctrl
import asyncio
import sys


#Set up the camera
cam_port = 0
cam = cv.VideoCapture(cam_port, cv.CAP_DSHOW)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 3264)          #set frame width (max res from data sheet)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 2558)          #set frame heigh (max res from data sheet)


petriCamLocations = [[66.11, 62.57], [66.11, -58.08], [180.41, 62.57], 
                      [180.41, -58.08], [294.71, 62.57], [409.01, 62.57]]


#Takes photos x amount of petri dishes (user specified) and saves to new folder
def takePhotos(folder_path, numPetriDishes):
    petriCounter = 0
    for i in range(1, numPetriDishes + 1):
        #move to petriLocations[petriCounter] to petriCamLocations[i]
        result, image = cam.read()
        print("----------IMAGE TAKEN----------")
        if result:
            imgName = f"petri_dish_{i}.jpg"
            cv.imwrite(imgName, image)
            img_path_to_save = os.path.join(folder_path, imgName)
            shutil.move(imgName, img_path_to_save)
        petriCounter = petriCounter + 1
    cam.release()

def main():
    #drive_ctrl = DriveManager()
    
    #Home
    #CPRmotorctrl.home()

    #Create a new folder for were photos will go
    imagesforProcessingFolder = "baseplatePhotos"
    os.makedirs(imagesforProcessingFolder)

    #TEMP: Manually addnig photos for test
    shutil.copy(os.path.join('image1.jpg'), os.path.join(imagesforProcessingFolder, 'image1.jpg'))
    shutil.copy(os.path.join('image2.jpg'), os.path.join(imagesforProcessingFolder, 'image2.jpg'))
    shutil.copy(os.path.join('image3.jpg'), os.path.join(imagesforProcessingFolder, 'image3.jpg'))
    shutil.copy(os.path.join('image4.jpg'), os.path.join(imagesforProcessingFolder, 'image4.jpg'))
    shutil.copy(os.path.join('image5.jpg'), os.path.join(imagesforProcessingFolder, 'image5.jpg'))
    shutil.copy(os.path.join('image6.jpg'), os.path.join(imagesforProcessingFolder, 'image6.jpg'))
    
    #Take Images of Petri Dishes
    numPetriDishes = 6  #TODO this should come from GUI
    #takePhotos(imagesforProcessingFolder, numPetriDishes)    #TODO will need to incorporate motor controls

    #call image processing using the folder created
    goodColoniesFolder = "goodColonies"
    os.makedirs(goodColoniesFolder)
    cpr.process_petri_dish_image(image_folder_path=imagesforProcessingFolder, good_colony_coord_output_path=goodColoniesFolder)
   
    #Randomize and select 96 colonies using images from new folder *produces sampledColoniesFolder
    coloniesToSample =CPR_random.randomize(goodColoniesFolder)  
    print(coloniesToSample) 
    
    #Execute tool path
    dwell_duration = 5 # TODO input from GUI
    #CPRmotorctrl.executeToolPath(coloniesToSample, dwell_duration)

    #callimage meta data with the images and colonies
    cpr.create_metadata(image_folder_path=imagesforProcessingFolder, colony_coords_folder_path='./sampleColonies', create_petri_dish_view=True, create_colony_view= True)

    #currently deleting the file after execution- will need to delete end of program
    #TODO place metadata into other folder/ access for user
    shutil.rmtree('goodColonies')  
    shutil.rmtree(imagesforProcessingFolder)
    shutil.rmtree('runs')
    shutil.rmtree('sampleColonies')
    shutil.rmtree('yolo_dump')
    
main()