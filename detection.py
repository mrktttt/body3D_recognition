import cv2
import mediapipe as mp
import time
import json
# Importation des fonctions locales
import positionFunctions as pf # Importation de la fonction locale. (positionFunctions.py)
from cameraCalibration import calibrate_camera # Importation de la fonction de calibration de la caméra.


# Sélection des os à afficher
# Indices des landmarks MediaPipe à afficher
# Ces indices correspondent aux points clés du corps que nous voulons visualiser.
# Ils sont basés sur la documentation de MediaPipe Pose.
# https://google.github.io/mediapipe/solutions/pose.html#pose-landmarks
# https://google.github.io/mediapipe/images/mobile/pose_tracking_full_body_landmarks.png
selected_landmarks = [
    # Visage
    0, 2, 5,
    # Épaules
    11, 12,
    # Coudes
    13, 14,
    # Poignets
    15, 16,
    # Hanches
    23, 24,
    # Genoux
    25, 26,
    # Chevilles
    27, 28,
    # Pieds
    29, 30
]

# Initialisation de la fenêtre d'affichage
cv2.namedWindow("Detection", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Detection", 1280, 720)  # Redimensionnement de la fenêtre
cv2.startWindowThread()

# Initialisation de MediaPipe pour la détection de pose
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Initialisation de la webcam
cap = cv2.VideoCapture(0)

"""
# Pour augementer la résolution de la webcam. Impact significatif sur les FPS.
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Définir la largeur
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Définir la hauteur
"""

# Variable utilisée pour le calcul des FPS
pTime = 0

# Calibration de la caméra 
camera_matrix, dist_coeffs = calibrate_camera()

# Liste pour stocker les données d'animations
animation_data = []
frame_count = 0

with pose:
    while cap.isOpened():

        # Lire une image de la webcam
        ret, frame = cap.read()

        # Dans le cas où webcan inaccessible.
        if not ret:
            print("Erreur lecture webcam")
            break
        
        # Conversion de l'image pour MediaPipe
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Affichage du FPS
        cTime = time.time() # Temps actuel
        fps = 1 / (cTime - pTime) # Calcul des FPS
        pTime = cTime # MAJ du temps précédent
        cv2.putText(image, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        
        # Dessiner les landmarks de la pose
        if results.pose_landmarks:
            # Pour le squelette complet (fourni par MediaPipe)
            # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Pour dessiner notre sélection d'os
            pf.draw_selected_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, selected_landmarks)

            # Extraction des coordonnées utilisables
            body_coordinates_3d = pf.extract_body_coordinates_3d(
                results.pose_landmarks, 
                image.shape, 
                camera_matrix, 
                dist_coeffs
            )

            # Export au format blender
            blender_frame_data = pf.export_to_blender_format(body_coordinates_3d, frame_count)
            animation_data.append(blender_frame_data)

            frame_count += 1

            # Vérifier la visibilité des points clés
            visible_points = 0
            total_points = len(body_coordinates_3d)
            
            for point_name, point_data in body_coordinates_3d.items():
                # MediaPipe considère un point comme "visible" si sa visibilité est > 0.5
                if point_data["visibility"] > 0.5:
                    visible_points += 1
            
            # Calculer le pourcentage de visibilité
            visibility_percentage = (visible_points / total_points) * 100
            
            # Afficher le pourcentage de visibilité
            visibility_text = f"Visibilité: {int(visibility_percentage)}%"
            cv2.putText(image, visibility_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Avertissement si moins de 90% des points sont visibles
            if visibility_percentage < 90:
                warning_text = "ATTENTION: Certains points ne sont pas visibles!"
                text_size = cv2.getTextSize(warning_text, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)[0]
                text_x = (image.shape[1] - text_size[0]) // 2  # Centre horizontalement
                
                # Afficher l'avertissement en rouge et en gras
                cv2.putText(image, warning_text, (text_x, 120), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        
        # Affichage des coordonnées des points sur l'image.
        cv2.imshow("Detection", image)

        # Quitter la boucle si 'q' est pressé
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Sauvegarder les données d'animation
with open('animation_data.json', 'w') as f:
    json.dump(animation_data, f, indent=2)

print(f"Animation sauvegardée avec {len(animation_data)} frames")

#Stop l'utilisation de la webcam et ferme les fenêtres
cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)


