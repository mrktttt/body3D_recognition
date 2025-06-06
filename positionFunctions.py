import cv2

# Fonction pour dessiner seulement certains os
def draw_selected_landmarks(image, landmarks, connections, selected_indices):
    """
    En fonction des indices sélectionnés, dessine les os correspondants sur l'image.

    Args:
        image: L'image sur laquelle dessiner les landmarks.
        landmarks: Les landmarks MediaPipe.
        connections: Les connexions entre les landmarks.
        selected_indices: Liste des indices des landmarks à dessiner.
    Returns:
        None
    """
    # Dessin des os sélectionnés uniquement
    for idx, landmark in enumerate(landmarks.landmark):
        if idx in selected_indices:
            h, w, c = image.shape
            cx, cy = int(landmark.x * w), int(landmark.y * h)
            cv2.circle(image, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
    
    # Dessin des connections entre les os sélectionnés
    for connection in connections:
        if connection[0] in selected_indices and connection[1] in selected_indices:
            start_idx, end_idx = connection
            start_landmark = landmarks.landmark[start_idx]
            end_landmark = landmarks.landmark[end_idx]
            
            h, w, c = image.shape
            start_point = (int(start_landmark.x * w), int(start_landmark.y * h))
            end_point = (int(end_landmark.x * w), int(end_landmark.y * h))
            
            cv2.line(image, start_point, end_point, (0, 255, 0), 2)


def extract_body_coordinates(landmarks, image_shape):
    """
    Extrait les coordonnées des points clés du corps dans un dictionnaire
    
    Args:
        landmarks: Les landmarks MediaPipe
        image_shape: Les dimensions de l'image (height, width, channels)
    
    Returns:
        Un dictionnaire contenant les coordonnées des points clés en pixels
    """
    h, w, _ = image_shape
    body_points = {}
    
    # Cartographie des indices aux noms de parties du corps
    landmark_names = {
        0: "nose", 
        2: "left_eye", 
        5: "right_eye",
        11: "left_shoulder", 
        12: "right_shoulder",
        13: "left_elbow", 
        14: "right_elbow",
        15: "left_wrist", 
        16: "right_wrist",
        23: "left_hip", 
        24: "right_hip",
        25: "left_knee", 
        26: "right_knee",
        27: "left_ankle", 
        28: "right_ankle",
        29: "left_foot", 
        30: "right_foot"
    }
    
    for idx, name in landmark_names.items():
        landmark = landmarks.landmark[idx]
        # Conversion des coordonnées normalisées en pixels
        x, y = int(landmark.x * w), int(landmark.y * h)
        # Stocker également la profondeur (z) - à noter que z n'est pas à l'échelle de l'image
        z = landmark.z
        # Ajouter la visibilité du point (confiance de détection)
        visibility = landmark.visibility
        
        body_points[name] = {
            "x": x,
            "y": y,
            "z": z,
            "visibility": visibility
        }
    
    return body_points