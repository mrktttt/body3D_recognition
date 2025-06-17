import cv2 as cv
import os
import sys

def capture_calibration_images(file_path, id_cam):
    """
    Capture des images avec un échiquier pour la calibration de la caméra.    
    Args:
        file_path : the file where we need to save the pictures. Used for two camera setup.
        id_cam : to choose with camera to use. Again used essentially for two camera setup.
    Returns:
        None
    """

    cap = cv.VideoCapture(id_cam)

    # Changing the resolution to the one we will be using next. 
    frame_shape = [720, 1280]
    
    cap.set(3, frame_shape[1])
    cap.set(4, frame_shape[0])

    # Créer le dossier pour stocker les images de calibration
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    
    img_counter = 0
    

    print("Appuyez sur ESPACE pour capturer une image, 'q' pour quitter")
    print("Capturez au moins 10-20 images de l'échiquier sous différents angles")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame.shape[1] != 720:
            frame = frame[:,frame_shape[1]//2 - frame_shape[0]//2:frame_shape[1]//2 + frame_shape[0]//2]

            
        cv.imshow('Capture - Appuyez sur ESPACE pour capturer', frame)
        
        key = cv.waitKey(1) & 0xFF
        
        if key == ord(' '):  # Espace pour capturer
            img_name = f"{file_path}/img_{img_counter:02d}.jpg"
            cv.imwrite(img_name, frame)
            print(f"Image sauvegardée: {img_name}")
            img_counter += 1
            
        elif key == ord('q'):  # 'q' pour quitter
            break
    
    cap.release()
    cv.destroyAllWindows()
    print(f"Capture terminée. {img_counter} images sauvegardées.")

if __name__ == "__main__":

    if len(sys.argv) == 3:
        file_path = str(sys.argv[1])
        id_cam = int(sys.argv[2])

    capture_calibration_images(file_path, id_cam)