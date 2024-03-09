import random
import os, glob
import shutil
import cv2 as cv
import time
import logging
from dataclasses import dataclass
import CPR_tools as cpr
import CPR_random
import CPRmotorctrl
import asyncio
from libmotorctrl import DriveManager, DriveTarget

TMP_DIRECTORIES = [
    "goodColonies",
    "baseplatePhotos",
    "pinHolePhoto",
    "runs",
    "sampleColonies",
    "yolo_dump",
    "metadata",
]


def main():
    for dir in TMP_DIRECTORIES:
        if os.path.exists(dir) and os.path.isdir(dir):
            logging.warning(
                "Deleting leftover tmp directory %s (did the last run finish successfully?)",
                dir,
            )
            shutil.rmtree(dir)

    drive_ctrl = DriveManager()
    asyncio.run(drive_ctrl.init_drives())
    logging.info("Drives initialized")

    # Home
    logging.info("Starting drive homing...")
    asyncio.run(drive_ctrl.home(DriveTarget.DriveZ))
    asyncio.run(drive_ctrl.home(DriveTarget.DriveX))
    asyncio.run(drive_ctrl.home(DriveTarget.DriveY))
    logging.info("Homing complete")

    # Manually set calibration
    CPRmotorctrl.calibrate(drive_ctrl, 15560, 125940)

    # Image pinhole
    logging.info("Starting calibration cycle...")
    os.makedirs("pinHolePhoto")
    asyncio.run(
        CPRmotorctrl.pinhole_capture(drive_ctrl, "pinHolePhoto")
    )  # TODO change this out of the temp folder to pinhole folder
    # offsetX, offsetY = cpr.pinhole('./pinHolePhoto/pinhole.jpg', save_image_path= './pinHolePhoto/pinhole.jpg', row_deviation_threshold=.1, column_deviation_threshold=.1, center_point=(0.5, 0.48))
    print("applying offset")  # TODO setcalibration offset

    # Capture Petri dish images
    logging.info("Capturing Petri dish images...")
    os.makedirs("baseplatePhotos")
    numPetriDishes = 6  # TODO this should come from GUI
    asyncio.run(CPRmotorctrl.takePhotos("baseplatePhotos", numPetriDishes, drive_ctrl))

    # create a folder where text files of good corddinates will be placed
    os.makedirs("goodColonies")
    cpr.process_petri_dish_image(
        image_folder_path="baseplatePhotos",
        good_colony_coord_output_path="goodColonies",
    )

    # Randomize and select 96 colonies using images from new folder
    # (produces sampleColonies directory containing images)
    coloniesToSample = CPR_random.randomize("goodColonies")

    # call image meta data with the file created above
    cpr.create_metadata(
        image_folder_path="baseplatePhotos",
        colony_coords_folder_path="./sampleColonies",
        create_petri_dish_view=True,
        create_colony_view=True,
    )

    # Perform sampling cycle
    dwell_duration = 5  # TODO input from GUI
    asyncio.run(
        CPRmotorctrl.executeToolPath(coloniesToSample, dwell_duration, drive_ctrl)
    )

    # currently deleting the file after execution- will need to delete end of program
    shutil.rmtree("goodColonies")
    shutil.rmtree("baseplatePhotos")
    shutil.rmtree("runs")
    shutil.rmtree("sampleColonies")
    shutil.rmtree("yolo_dump")


main()
