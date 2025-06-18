import cv2 as cv 
import glob
import numpy as np
import matplotlib.pyplot as plt

# Based on : http://temugeb.github.io/opencv/python/2021/02/02/stereo-camera-calibration-and-triangulation.html


def calibrate_camera(images_folder):
    """
    This function calibrates a camera using a set of chessboard images.

    Parameters:
    images_folder (str): Path to the folder containing chessboard images.
    
    Returns:
    tuple: Camera matrix and distortion coefficients.

    """
    images_names = glob.glob(images_folder)
    images = []
    for imname in images_names:
        img = cv.imread(imname, 1)
        images.append(img)

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    rows = 4
    columns = 7
    world_scaling = 1

    objp = np.zeros((rows * columns, 3), np.float32)
    objp[:,:2] = np.mgrid[0:rows, 0:columns].T.reshape(-1, 2)
    objp *= world_scaling
    
    #thoses are the dimensions of the images we will use
    width = 720 #images[0].shape[1] 
    height = 720 #images[0].shape[0]

    imgpoints = []
    objpoints = []
    
    for img in images:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        ret, corners = cv.findChessboardCorners(gray, (rows, columns), None)

        if ret:
            conv_size = (11, 11)
            corners = cv.cornerSubPix(gray, corners, conv_size, (-1, -1), criteria)
            cv.drawChessboardCorners(img, (rows, columns), corners, ret)
            cv.imshow('img', img)
            k = cv.waitKey(500)
            objpoints.append(objp)
            imgpoints.append(corners)

    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, (width, height), None, None)
    print ('rmse:', ret)
    print('camera matrix:\n', mtx)
    print('Rs:\n', rvecs)
    print('Ts:\n', tvecs)

    return mtx, dist
        

def calibrate_stereo (images_folder1, images_folder2):
    """
    This function calibrates a stereo camera system using two sets of chessboard images.

    The cameras pictures needs to be taken at the same time. Therefore, make sure to be synchronised when taking the pictures.
    parameters :   
        images_folder1 (str): Path to the folder containing chessboard images for camera 1.
        images_folder2 (str): Path to the folder containing chessboard images for camera 2. 
    """
    
    img_names1 = glob.glob(images_folder1)
    img_names2 = glob.glob(images_folder2)
    c1_images = []
    c2_images = []

    for imname in img_names1:
        img = cv.imread(imname, 1)
        c1_images.append(img)
    for imname in img_names2:  
        img = cv.imread(imname, 1)
        c2_images.append(img)
    


if __name__ == '__main__':
    mtx1, dist1 = calibrate_camera("calib_c1/*.jpg")
    mtx2, dist2 = calibrate_camera("calib_c2/*.jpg")

    print(mtx1, dist1, mtx2, dist2)