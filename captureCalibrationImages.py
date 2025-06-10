import cv2
import os

def capture_calibration_images():
    """
    Capture des images avec un échiquier pour la calibration de la caméra.    
    Args:
        bNone
    Returns:
        None
    """
    cap = cv2.VideoCapture(0)
    
    # Créer le dossier pour stocker les images de calibration
    if not os.path.exists('calibration_images'):
        os.makedirs('calibration_images')
    
    img_counter = 0
    
    print("Appuyez sur ESPACE pour capturer une image, 'q' pour quitter")
    print("Capturez au moins 10-20 images de l'échiquier sous différents angles")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        cv2.imshow('Capture - Appuyez sur ESPACE pour capturer', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):  # Espace pour capturer
            img_name = f"calibration_images/calibration_{img_counter:02d}.jpg"
            cv2.imwrite(img_name, frame)
            print(f"Image sauvegardée: {img_name}")
            img_counter += 1
            
        elif key == ord('q'):  # 'q' pour quitter
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print(f"Capture terminée. {img_counter} images sauvegardées.")

if __name__ == "__main__":
    capture_calibration_images()