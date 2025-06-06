import cv2
import numpy as np

def calibrate_camera():
    """
    Calibre la caméra pour obtenir les paramètres intrinsèques
    Retourne la matrice de la caméra et les coefficients de distorsion
    """
    # Cette fonction nécessite un processus de calibration avec un échiquier
    # Pour l'exemple, voici des valeurs approximatives pour une webcam standard
    camera_matrix = np.array([[800, 0, 320],
                             [0, 800, 240],
                             [0, 0, 1]], dtype=np.float32)
    
    dist_coeffs = np.array([0.1, -0.2, 0, 0, 0], dtype=np.float32)
    
    return camera_matrix, dist_coeffs
