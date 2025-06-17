import cv2 as cv
import mediapipe as mp
import numpy as np

"""
Ce script permet de détecter les caméras disponibles sur le système.
Il essaie de se connecter à chaque caméra de l'index 0 à 4.
Si une caméra est trouvée, son index est affiché.
"""
for i in range(5):
    cap = cv.VideoCapture(i)
    if cap.read()[0]:
        print(f"Caméra trouvée à l'index {i}")
        cap.release()
