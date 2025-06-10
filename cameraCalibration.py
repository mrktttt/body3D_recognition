import cv2
import numpy as np
import glob
import pickle
import os

def calibrate_camera():
    """
    Calibre la caméra pour obtenir les paramètres intrinsèques
    Retourne la matrice de la caméra et les coefficients de distorsion
    """
    
    # Vérifier si une calibration existe déjà
    if os.path.exists('camera_calibration.pkl'):
        print("Calibration existante trouvée, chargement...")
        with open('camera_calibration.pkl', 'rb') as f:
            calibration_data = pickle.load(f)
        return calibration_data['camera_matrix'], calibration_data['dist_coeffs']
    
    # Critères de terminaison
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    # Préparer les points de l'échiquie r (7x6 intersections internes)
    objp = np.zeros((4*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:7,0:4].T.reshape(-1,2)
    
    # Arrays pour stocker les points
    objpoints = [] # Points 3D dans l'espace réel
    imgpoints = [] # Points 2D dans le plan image
    
    # Charger les images de calibration
    images = glob.glob('calibration_images/*.jpg')
    
    if len(images) == 0:
        print("Aucune image de calibration trouvée dans 'calibration_images/'")
        print("Lancez d'abord capture_calibration_images.py")
        # Retourner des valeurs par défaut
        camera_matrix = np.array([[800, 0, 320],
                                 [0, 800, 240],
                                 [0, 0, 1]], dtype=np.float32)
        dist_coeffs = np.array([0.1, -0.2, 0, 0, 0], dtype=np.float32)
        return camera_matrix, dist_coeffs
    
    print(f"Traitement de {len(images)} images de calibration...")
    
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Trouver les coins de l'échiquier
        ret, corners = cv2.findChessboardCorners(gray, (7,4), None)
        
        # Si trouvé, ajouter les points
        if ret == True:
            objpoints.append(objp)
            
            # Affiner la position des coins
            corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners2)
            
            # Dessiner et afficher les coins (optionnel)
            cv2.drawChessboardCorners(img, (7,4), corners2, ret)
            cv2.imshow('Corners détectés', img)
            cv2.waitKey(100)
        else:
            print(f"Échec détection échiquier dans {fname}")
    
    cv2.destroyAllWindows()
    
    if len(objpoints) == 0:
        print("Aucun échiquier détecté dans les images!")
        # Retourner des valeurs par défaut
        camera_matrix = np.array([[800, 0, 320],
                                 [0, 800, 240],
                                 [0, 0, 1]], dtype=np.float32)
        dist_coeffs = np.array([0.1, -0.2, 0, 0, 0], dtype=np.float32)
        return camera_matrix, dist_coeffs
    
    print(f"Calibration avec {len(objpoints)} images valides...")
    
    # Calibration de la caméra
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None)
    
    if ret:
        print("Calibration réussie!")
        print(f"Erreur de reprojection: {ret}")
        print(f"Matrice caméra:\n{camera_matrix}")
        print(f"Coefficients de distorsion: {dist_coeffs.ravel()}")
        
        # Sauvegarder la calibration
        calibration_data = {
            'camera_matrix': camera_matrix,
            'dist_coeffs': dist_coeffs,
            'reprojection_error': ret
        }
        
        with open('camera_calibration.pkl', 'wb') as f:
            pickle.dump(calibration_data, f)
        
        print("Calibration sauvegardée dans 'camera_calibration.pkl'")
        
        return camera_matrix, dist_coeffs
    else:
        print("Échec de la calibration!")
        # Retourner des valeurs par défaut
        camera_matrix = np.array([[800, 0, 320],
                                 [0, 800, 240],
                                 [0, 0, 1]], dtype=np.float32)
        dist_coeffs = np.array([0.1, -0.2, 0, 0, 0], dtype=np.float32)
        return camera_matrix, dist_coeffs

def test_calibration():
    """
    Test de la calibration avec une image en temps réel
    """
    camera_matrix, dist_coeffs = calibrate_camera()
    
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Image non corrigée
        h, w = frame.shape[:2]
        
        # Nouvelle matrice de caméra pour l'image corrigée
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(
            camera_matrix, dist_coeffs, (w,h), 1, (w,h))
        
        # Correction de la distorsion
        undistorted = cv2.undistort(frame, camera_matrix, dist_coeffs, None, newcameramtx)
        
        # Affichage côte à côte
        combined = np.hstack((frame, undistorted))
        cv2.putText(combined, "Original", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(combined, "Corrigé", (w + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow('Test Calibration - Appuyez sur q pour quitter', combined)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("1. Calibration de la caméra")
    print("2. Test de la calibration")
    choice = input("Choisissez (1 ou 2): ")
    
    if choice == "1":
        calibrate_camera()
    elif choice == "2":
        test_calibration()