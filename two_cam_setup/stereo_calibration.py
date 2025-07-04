import cv2 as cv 
import glob
import numpy as np

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
            k = cv.waitKey(50)
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
        mtx1 : camera matrix for cam 1
        dist1 : distortion coefficients for cam 1
        mtx2 : camera matrix for cam 2
        dist2 : distortion coefficients for cam 2
        images_folder1 (str): Path to the folder containing chessboard images for camera 1.
        images_folder2 (str): Path to the folder containing chessboard images for camera 2. 
    returns :
        R (np.ndarray): Rotation matrix between the two cameras.
        T (np.ndarray): Translation vector between the two cameras.
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
            cv.drawChessboardCorners(frame2, (rows, columns), corners2, ret2)
            
            # Ajouter des labels sur chaque frame
            cv.putText(frame1, "Camera 0", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv.putText(frame2, "Camera 1", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            combined_frame = np.hstack((frame1, frame2))
            cv.imshow('Calibration stereo', combined_frame)

            cv.waitKey(50)

            objpoints.append(objp)
            imgpoints_left.append(corners1)
            imgpoints_right.append(corners2)

    stereocalibration_flags = cv.CALIB_FIX_INTRINSIC
    ret, CM1, dist1, CM2, dist2, R, T, E, F = cv.stereoCalibrate(objpoints, imgpoints_left, imgpoints_right, mtx1, dist1, mtx2, dist2, (width, height), criteria=criteria, flags=stereocalibration_flags)
    print(ret)
    return R, T


def DLT (P1, P2, pt1, pt2):
    """
    This function implements the Direct Linear Transform (DLT) algorithm to compute the fundamental matrix.

    Parameters:
    P1 (np.ndarray): Camera matrix for camera 1.
    P2 (np.ndarray): Camera matrix for camera 2.
    pt1 (np.ndarray): Points in image 1.
    pt2 (np.ndarray): Points in image 2.

    Returns:
    np.ndarray: Fundamental matrix.
    """
    A = [pt1[1]*P1[2,:] - P1[1,:],
         P1[0,:] - pt1[0]*P1[2,:],
         pt2[1]*P2[2,:] - P2[1,:],
         P2[0,:] - pt2[0]*P2[2,:]]
    print('A before reshape: ', A)
    A = np.array(A).reshape((3,4))
    print('A: ')
    print(A)

    B = A.transpose() @ A
    from scipy import linalg 
    U, s, Vh = linalg.svd(B, full_matrices = False)

    print('Triangulated point: ')
    print(Vh[3,0:3]/ Vh[3,3])
    return Vh[3,0:3]/ Vh[3,3]

if __name__ == '__main__':
    mtx1, dist1 = calibrate_camera("c1/*.png")
    mtx2, dist2 = calibrate_camera("c2/*.png")

    print(mtx1, dist1, mtx2, dist2)

    R, T = calibrate_stereo(mtx1, dist1, mtx2, dist2, "c1/*.png", "c2/*.png")

    R1, T1 = calibrate_stereo(mtx2, dist2, mtx1, dist1, "c2/*.png", "c1/*.png")
    print("R:\n", R)
    print("T:\n", T)
    print("R1:\n", R1)
    print("T1:\n", T1)

    
    # DU BON GROS HARDCODED POUR LA PASSION DE LA PASSION DU FUN.
    uvs1 = [[458, 86], [451, 164], [287, 181],
            [196, 383], [297, 444], [564, 194],
            [562, 375], [596, 520], [329, 620],
            [488, 622], [432, 52], [489, 56]]

    uvs2 = [[540, 311], [603, 359], [542, 378],
            [525, 507], [485, 542], [691, 352],
            [752, 488], [711, 605], [549, 651],
            [651, 663], [526, 293], [542, 290]]

    points3D = []
    for uv1, uv2 in zip(uvs1, uvs2):
        print(uv1, uv2)
        point3D = DLT(mtx1, mtx2, uv1, uv2)
        points3D.append(point3D)
    points3D = np.array(points3D)
    print("3D Points:\n", points3D)

