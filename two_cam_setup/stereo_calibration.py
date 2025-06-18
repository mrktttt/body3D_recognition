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
        

def calibrate_stereo (mtx1, dist1, mtx2, dist2, images_folder1, images_folder2):
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
        img1 = cv.imread(imname, 1)
        c1_images.append(img1)
    for imname in img_names2:  
        img2 = cv.imread(imname, 1)
        c2_images.append(img2)

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.0001)

    rows = 4
    columns = 7
    world_scaling = 1
    
    objp = np.zeros((rows * columns, 3), np.float32)
    objp[:,:2] = np.mgrid[0:rows, 0:columns].T.reshape(-1, 2)
    objp *= world_scaling

    width = 720 #c1_images[0].shape[1]
    height = 720 #c1_images[0].shape[0]

    imgpoints_left = []
    imgpoints_right = []

    objpoints = []

    for frame1, frame2 in zip(c1_images, c2_images):
        gray1 = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
        gray2 = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
        ret1, corners1 = cv.findChessboardCorners(gray1, (rows, columns), None)
        ret2, corners2 = cv.findChessboardCorners(gray2, (rows, columns), None)

        if ret1 and ret2:
            conv_size = (11, 11)
            corners1 = cv.cornerSubPix(gray1, corners1, conv_size, (-1, -1), criteria)
            corners2 = cv.cornerSubPix(gray2, corners2, conv_size, (-1, -1), criteria)
    
            cv.drawChessboardCorners(frame1, (rows, columns), corners1, ret1)
            cv.imshow('img1', frame2)
            cv.drawChessboardCorners(frame2, (rows, columns), corners2, ret2)
            cv.imshow('img2', frame1)

            k = cv.waitKey(0)

            objpoints.append(objp)
            imgpoints_left.append(corners1)
            imgpoints_right.append(corners2)

    stereocalibration_flags = cv.CALIB_FIX_INTRINSIC
    ret, CM1, dist1, CM2, dist2, R, T, E, F = cv.stereoCalibrate(objpoints, imgpoints_left, imgpoints_right, mtx1, dist1, mtx2, dist2, (width, height), criteria=criteria, flags=stereocalibration_flags)
    print(ret)
    return R, T




if __name__ == '__main__':
    mtx1, dist1 = calibrate_camera("calib_c1/*.jpg")
    mtx2, dist2 = calibrate_camera("calib_c2/*.jpg")

    print(mtx1, dist1, mtx2, dist2)

    R, T = calibrate_stereo(mtx1, dist1, mtx2, dist2, "c1/*.jpg", "c2/*.jpg")

    print("R:\n", R)
    print("T:\n", T)