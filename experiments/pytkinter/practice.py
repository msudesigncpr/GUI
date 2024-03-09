from msilib.schema import _Validation_records
import cv2 as cv
import numpy as np
import openpyxl
import time
import threading

#set up camera
cam_port = 0
cam = cv.VideoCapture(cam_port, cv.CAP_DSHOW)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 3264)          #set frame width (max res from data sheet)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 2558)          #set frame heigh (max res from data sheet)

#Un-distort, arrays came from calibarate funtions in calibrate.py file
DIM= (3264, 2448)
K=np.array([[441830.0440255356, 0.0, 852.1256225236111], [0.0, 516414.51234938996, 1245.8722842811067], [0.0, 0.0, 1.0]])
D=np.array([[-882.310014580582], [590380.1877261768], [231827527.76974776], [-2385332774656.0986]])

#shrinks an image
def rescaleFrame(frame, scale):
        width = int(frame.shape[1] * scale)
        height = int(frame.shape[0] * scale)
        dimensions = (width, height)

        #change resolution so that it is 2.6Mp(for image processing)/8Mp (Camera) 0.033 
       
        frame =  cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)
        #return rescaleFrame(frame, 3)

def crop(frame):
        croppedImage = frame[1024:50, 768:50]
        return croppedImage

def toCricle(resizedImage):
        blank = np.zeros(resizedImage.shape[:2], dtype='uint8')
        mask = cv.circle(blank, (resizedImage.shape[1]//2 + 0, resizedImage.shape[0]//2 + 0), 200, 255, -1) #(a, b, c, d, e), c changed size of circle
        maskedImage = cv.bitwise_and(resizedImage, resizedImage, mask=mask)
        cv.imshow('Mask', maskedImage)
        cv.waitKey(0)
        
        return maskedImage

#Undistort funtion uses calibarate function to account for 72 degree fisheye
def undistort(img_path):
    img = cv.imread(img_path)
    h,w = img.shape[:2]
    map1, map2 = cv.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv.CV_16SC2)
    undistorted_img = cv.remap(img, map1, map2, interpolation=cv.INTER_LINEAR, borderMode=cv.BORDER_CONSTANT)
    
    return undistorted_img

#def dilute(img_path) this will create an image that can change the resolution for Johns processing

#function to take an image, undistort it with given arrays, resize image, return path to final image
def takeImage(scale):
        start_time = time.time()  # Capture the initial time
        image_taken = False

        while True:
                current_time = time.time()
                elapsed_time = current_time - start_time

                if elapsed_time >= 5 and not image_taken:
                        result, image = cam.read()
                        print("----------IMAGE TAKEN----------")
                
                        if result:
                                timeStamp = int(time.time())
                                imgName = f"NewImage{timeStamp}.jpg"
                                cv.imwrite(imgName, image)

                                undistorted = undistort(imgName)
                                cv.imwrite(f"undistorted{timeStamp}.jpg", undistorted)

                                resizedImage = rescaleFrame(undistorted, scale)
                                cv.imwrite(f"resized{timeStamp}.jpg", resizedImage)

                                return f"resized{timeStamp}.jpg"
                        else:
                                print("No image detected")
                                return None

                # Check for a new petri dish location and reset the timer
                if elapsed_time >= 5:
                        start_time = time.time()
                        image_taken = False

#Function to print image to excel file
def toExcel(workbook, name, img):
        worksheet = workbook.create_sheet(title=name)
        worksheet['A1'] = "Adding image from cam"
        img = openpyxl.drawing.image.Image(img)       #image saved within this working directory
        img.anchor = 'A2'
        worksheet.add_image(img)

def main():
        #take image (scale)
        #Load workbook
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = 'Intro'
        worksheet['A1'] = "Each page is for a new Petri Dish"

        numPetriDishes = 1
        scale = 0.1
        for i in range(1, numPetriDishes + 1):
                imgPath = takeImage(scale)
                #open and send to existing Excel file
                if imgPath:
                        sheetName = f'Petridish{i}'
                        toExcel(workbook, sheetName, imgPath) 
        workbook.save('practice.xlsx')
main()
cv.waitKey(0)