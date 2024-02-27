import os, glob
import shutil
#from libmotorctrl import DriveOverseer, DriveTarget
import CPR_tools as cpr
import CPR_random
#import CPRmotorctrl
#from constants import *


def main():
    #drive_ctrl = DriveManager()
    
    #Home
    #CPRmotorctrl.home()

    #apply any offset
    #move to pinhole
    #take an image
    #cpr.pinhole('./pinhole_test_images/pinhole_lights_on.jpg', save_image_path= './pinhole_test.jpg', row_deviation_threshold=.1, column_deviation_threshold=.1, center_point=(0.5, 0.48))

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
    #CPRmotorctrl.takePhotos(imagesforProcessingFolder, numPetriDishes, drive_ctrl)    #TODO will need to incorporate motor controls

    #call image processing using the folder created
    goodColoniesFolder = "goodColonies"
    os.makedirs(goodColoniesFolder)
    cpr.process_petri_dish_image(image_folder_path=imagesforProcessingFolder, good_colony_coord_output_path=goodColoniesFolder)
   
    #Randomize and select 96 colonies using images from new folder *produces sampledColoniesFolder
    coloniesToSample =CPR_random.randomize(goodColoniesFolder)  
    print(coloniesToSample) 
    
    #Execute tool path
    dwell_duration = 5 # TODO input from GUI
    #CPRmotorctrl.executeToolPath(coloniesToSample, dwell_duration) TODO double check right

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