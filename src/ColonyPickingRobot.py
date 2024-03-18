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
    "valid_colony_list",
    "petri_dish_photos_raw",
    "pinhole_photo",
    "runs",
    "target_colony_list",
    "petri_dish_photos_marked",
    "metadata",
]


def main():
    dwell_duration = 5  # TODO input from GUI
    petri_dish_count = 6  # TODO this should come from GUI

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
    os.makedirs("pinhole_photo")
    asyncio.run(
        CPRmotorctrl.pinhole_capture(drive_ctrl, "pinhole_photo")
    )  # TODO change this out of the temp folder to pinhole folder
    # offsetX, offsetY = cpr.pinhole('./pinhole_photo/pinhole.jpg', save_image_path= './pinhole_photo/pinhole.jpg', row_deviation_threshold=.1, column_deviation_threshold=.1, center_point=(0.5, 0.48))
    print("applying offset")  # TODO setcalibration offset

    # Capture Petri dish images
    logging.info("Capturing Petri dish images...")
    os.makedirs("petri_dish_photos_raw")
    asyncio.run(
        CPRmotorctrl.take_petri_dish_photos(
            "petri_dish_photos_raw", petri_dish_count, drive_ctrl
        )
    )

    # create a folder where text files of good corddinates will be placed
    os.makedirs("valid_colony_list")
    cpr.process_petri_dish_image(
        image_folder_path="petri_dish_photos_raw",
        good_colony_coord_output_path="valid_colony_list",
        raw_yolo_dump_path="./petri_dish_photos_marked",
    )

    # Randomize and select 96 colonies using images from new folder
    # (produces target_colony_list directory containing images)
    coloniesToSample = CPR_random.randomize("valid_colony_list")

    # call image meta data with the file created above
    cpr.create_metadata(
        image_folder_path="petri_dish_photos_raw",
        colony_coords_folder_path="target_colony_list",
        create_petri_dish_view=True,
        create_colony_view=True,
    )

    # Perform sampling cycle
    asyncio.run(
        CPRmotorctrl.execute_tool_path(coloniesToSample, dwell_duration, drive_ctrl)
    )

    # currently deleting the file after execution- will need to delete end of program
    shutil.rmtree("valid_colony_list")
    shutil.rmtree("petri_dish_photos_raw")
    shutil.rmtree("runs")
    shutil.rmtree("target_colony_list")


main()
