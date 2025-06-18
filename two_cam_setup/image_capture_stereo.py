import cv2 as cv
import os 
import numpy as np
import sys

def capture_image_stereo(file_path, id_cam1, id_cam2):
    """
    Capture des images avec deux caméras pour la calibration stéréo.
    Parameters : 
        file_path1: The path to the folder of images for the first cam.
        file_path2: The path to the folder of images for the second cam.
        id_cam1: The ID of the first camera.
        id_cam2: The ID of the second camera.
    Returns:
        None
    """
    cap1 = cv.VideoCapture(id_cam1)
    cap2 = cv.VideoCapture(id_cam2)
    caps = [cap1, cap2]

    # Changing the resolution to the one we will be using next. 
    frame_shape = [720, 1280]

    for cap in caps:
        cap.set(3, frame_shape[1])
        cap.set(4, frame_shape[0])

    # Créer les dossiers pour stocker les images de calibration
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    img_counter = 0

    print("Appuyez sur ESPACE pour capturer une image, 'q' pour quitter")
    print("Capturez au moins 10-20 images de l'échiquier sous différents angles")

    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        # Dans le cas où les caméras ne sont pas accessibles.
        if not ret1 or not ret2:
            break

        # Crop to 720x720.
        if frame1.shape[1] != 720:
            frame1 = frame1[:, frame_shape[1] // 2 - frame_shape[0] // 2: frame_shape[1] // 2 + frame_shape[0] // 2]
        
        if frame2.shape[1] != 720:
            frame2 = frame2[:, frame_shape[1] // 2 - frame_shape[0] // 2: frame_shape[1] // 2 + frame_shape[0] // 2]

        # Ajouter des labels sur chaque frame
        cv.putText(frame1, "Camera 0", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv.putText(frame2, "Camera 1", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        combined_frame = np.hstack((frame1, frame2))

        cv.imshow('Capture - Appuyez sur ESPACE pour capturer', combined_frame)

        key = cv.waitKey(1) & 0xFF

        if key == ord(' '):
            img_name1 = f"{file_path}/img_{img_counter:02d}.jpg"

            img_counter += 1

            img_name2 = f"{file_path}/img_{img_counter:02d}.jpg"

            cv.imwrite(img_name1, frame1)
            cv.imwrite(img_name2, frame2)
            print(f"Images sauvegardées: {img_name1} et {img_name2}")
            img_counter += 1

        elif key == ord('q'): 
            break

    cv.destroyAllWindows()
    for cap in caps:
        cap.release()

    print(f"Capture terminée. {img_counter} images sauvegardées dans {file_path}.")

if __name__ == "__main__":

    if len(sys.argv) == 4:
        file_path = sys.argv[1]
        id_cam1 = int(sys.argv[2])
        id_cam2 = int(sys.argv[3])

        capture_image_stereo(file_path, id_cam1, id_cam2)
    
    else:
        print("Il faut mettre des arguments.")