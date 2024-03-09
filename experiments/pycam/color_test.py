# Read the template and target images
# template = cv2.imread('color_board.jpg')
# target = cv2.imread('color_board.jpg')
# # Convert BGR to HSV color space
# template_hsv = cv2.cvtColor(template, cv2.COLOR_BGR2HSV)
# target_hsv = cv2.cvtColor(target, cv2.COLOR_BGR2HSV)
# # Define range of red color in HSV
# lower_red = np.array([0, 100, 100])
# upper_red = np.array([10, 255, 255])
# # Threshold the HSV images to get only red colors
# mask_template = cv2.inRange(template_hsv, lower_red, upper_red)
# mask_target = cv2.inRange(target_hsv, lower_red, upper_red)
# # Find contours in the thresholded images
# contours_template, _ = cv2.findContours(mask_template, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# contours_target, _ = cv2.findContours(mask_target, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# # Filter contours based on your criteria (e.g., size, shape)
# # Here, assuming the red dot is a small circular object
# filtered_contours = [cnt for cnt in contours_target if cv2.contourArea(cnt) < 1600]
# # Extract coordinates of the red dot from the contours
# for cnt in filtered_contours:
#     # Get the coordinates of the centroid of the contour
#     M = cv2.moments(cnt)
#     if M[""] != 0:
#         cX = int(M["m10"] / M["m00"])
#         cY = int(M["m01"] / M["m00"])
#         print(f"Coordinates of red dot: ({cX}, {cY})")

import cv2
import numpy as np
from PIL import Image

image = Image.open("color_board.jpg")
width, height = image.size
# Load image

pixval = list(image.getdata())

temp = []
hexcolpix = []
for row in range(0, height, 1):
    for col in range(0, width, 1):
        index = row * width + col
        temp.append(pixval[index])
    hexcolpix.append(temp)
    temp = []
