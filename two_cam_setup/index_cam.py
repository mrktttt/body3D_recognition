import cv2 as cv

"""
FR:
Ce script détecte les cameras/webcam disponibles sur le système. Il essaie de se connecter à chaque caméra de l'index 0 à 4. Si une caméra est trouvée, son index sera affiché.
--------------------------------------------------------------------------------------------
EN:
This script detects available cameras/webcams on the system. It attempts to connect to each camera from index 0 to 4. If a camera is found, its index will be displayed.
"""

cam_index = []
for i in range(5):
    #Tentative de connexion à la caméra à l'index i
    #Trying to connect to the camera at index i
    cap = cv.VideoCapture(i)

    # Vérifier si la caméra est ouverte avec succès
    # Check if the camera is opened successfully
    if cap.read()[0]:
        print(f"Caméra trouvée à l'index {i}")
        cam_index.append(i)
        cap.release()
    else:
        print(f"Aucune caméra trouvée à l'index {i}")
    
print(f"Caméras disponibles: {cam_index}")
