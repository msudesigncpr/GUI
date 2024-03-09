# Import required modules
import cv2
import numpy as np
import os
import glob

DIM = (3264, 2448)
K = np.array(
    [
        [441830.0440255356, 0.0, 852.1256225236111],
        [0.0, 516414.51234938996, 1245.8722842811067],
        [0.0, 0.0, 1.0],
    ]
)
D = np.array(
    [
        [-882.310014580582],
        [590380.1877261768],
        [231827527.76974776],
        [-2385332774656.0986],
    ]
)


def undistort(img_path):
    img = cv2.imread(img_path)
    h, w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(
        K, D, np.eye(3), K, DIM, cv2.CV_16SC2
    )
    undistorted_img = cv2.remap(
        img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT
    )
    cv2.imshow("undistorted", img)

    width = int(undistorted_img.shape[1] * 1)
    height = int(undistorted_img.shape[0] * 1)
    dimensions = (width, height)
    img = cv2.resize(undistorted_img, dimensions, interpolation=cv2.INTER_AREA)

    cv2.imwrite("undistorted_board.jpg", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


image = "TB_Points_Warped.jpg"
image = undistort(image)
