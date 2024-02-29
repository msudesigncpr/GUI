
import asyncio
import logging
import sys
from libmotorctrl import DriveManager, DriveTarget
from constants import *
import cv2 as cv
import numpy as np
import os, glob
import shutil


LOGLEVEL = logging.INFO

#Set up the camera
cam_port = 0
cam = cv.VideoCapture(cam_port, cv.CAP_DSHOW)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 3264)          #set frame width (max res from data sheet)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 2558)          #set frame heigh (max res from data sheet)


logging.basicConfig(
    format="%(asctime)s: %(threadName)s: %(message)s",
    level=LOGLEVEL,
    datefmt="%H:%M:%S",
)

async def home(drive_ctrl):
    await drive_ctrl.init_drives()
    logging.info("Drives initialized")

    await drive_ctrl.home(DriveTarget.DriveZ)
    await drive_ctrl.home(DriveTarget.DriveX)
    await drive_ctrl.home(DriveTarget.DriveY)
    logging.info("Homing complete")

#Takes photos x amount of petri dishes (user specified) and saves to new folder
async def takePhotos(folder_path, numPetriDishes, drive_ctrl):
    i = 0
    logging.info("Starting receiving images of Petri dishes...")
    for petri in IMAGE_COORDINATES:
        if(i < numPetriDishes):
            await drive_ctrl.move(int(petri[0] * 10**3), int(petri[1] * 10**3), CAMERA_POS_OFFSET)
            result, image = cam.read()
            print("----------IMAGE TAKEN----------")
            if result:
                imgName = f"petri_dish_{i}.jpg"
                cv.imwrite(imgName, image)
                img_path_to_save = os.path.join(folder_path, imgName)
                shutil.move(imgName, img_path_to_save)
            i += 1
    cam.release()

async def executeToolPath(valid_colonies_raw, dwell_duration, drive_ctrl):
    target_colonies = []
    for colony in valid_colonies_raw:
        target_colonies.append(Colony(dish="P0", x=colony[0], y=colony[1]))
        # TODO P0 is a placeholder; ideally this should come from parsing the
        # colony list so we always know which colony the sample originated from

    logging.info("Target colonies list acquired!")

    logging.info("Performing initial sterilization...")
    await drive_ctrl.move(
        STERILIZER_COORDINATES[0],
        STERILIZER_COORDINATES[1],
        STERILIZER_COORDINATES[2],
    )
    logging.info("Sleeping for %s seconds...", dwell_duration)
    await asyncio.sleep(dwell_duration)

    for colony in target_colonies:
        logging.info("Starting sampling cycle...")
        logging.info(
            f"Target colony is at {colony.x:.2f}, {colony.y:.2f} in Petri dish {colony.dish}"
        )
        # Find the target well
        well_target = None
        for well_candidate in WELLS:
            if not well_candidate.has_sample:
                well_target = well_candidate
                logging.info("Target well is %s", well_target.id)
                break
        if well_target is None:
            logging.error("No unused wells!")  # TODO Handle differently
            sys.exit(1)
        # Target well has been found, execute sampling run
        await drive_ctrl.move(
            int(colony.x * 10**3), int(colony.y * 10**3), PETRI_DISH_DEPTH
        )
        logging.info("Colony collected, moving to well...")
        await drive_ctrl.move(
            int(well_target.x * 10**3), int(well_target.y * 10**3), WELL_DEPTH
        )
        logging.info("Well reached, moving to sterilizer...")
        well_target.has_sample = True
        well_target.origin = colony.dish
        await drive_ctrl.move(
            STERILIZER_COORDINATES[0],
            STERILIZER_COORDINATES[1],
            STERILIZER_COORDINATES[2],
        )
        logging.info("Sleeping for %s seconds...", dwell_duration)
        await asyncio.sleep(dwell_duration)

    logging.info("Sampling complete!")
    await drive_ctrl.move(490_000, -90_000, 0)
    await drive_ctrl.terminate()