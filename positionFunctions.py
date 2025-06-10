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


def extract_body_coordinates_3d(landmarks, image_shape, camera_matrix, reference_depth=1.0):
    """
    Extrait les coordonnées 3D des points clés du corps dans l'espace réel
    
    Args:
        landmarks: Les landmarks MediaPipe
        image_shape: Les dimensions de l'image (height, width, channels)
        camera_matrix: Matrice intrinsèque de la caméra        reference_depth: Profondeur de référence en mètres
    
    Returns:
        Un dictionnaire contenant les coordonnées 3D en mètres
    """
    h, w, _ = image_shape
    body_points_3d = {}
    
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
        
        # Coordonnées en pixels
        x_px, y_px = int(landmark.x * w), int(landmark.y * h)
        
        # Utiliser la coordonnée z de MediaPipe comme profondeur relative
        # MediaPipe donne z en unités relatives à la largeur des hanches
        depth_relative = landmark.z
        depth_real = reference_depth + (depth_relative * 0.5)  # Ajustement empirique
        
        # Conversion des coordonnées pixel vers coordonnées 3D réelles
        # Utilisation de la matrice inverse de la caméra
        fx, fy = camera_matrix[0, 0], camera_matrix[1, 1]
        cx, cy = camera_matrix[0, 2], camera_matrix[1, 2]
        
        # Coordonnées 3D en mètres
        x = (x_px - cx) * depth_real / fx
        y = (y_px - cy) * depth_real / fy
        z = depth_real
        
        body_points_3d[name] = {
            "x": x,
            "y": y, 
            "z": z,
            "visibility": landmark.visibility
        }
    
    return body_points_3d

def export_to_blender_format(body_coordinates_3d, frame_number):
    """
    Exporte les coordonnées en 3 dimensions au format utilisable via Blender
    
    Args:
        body_coordinates_3d: Dictionnaire des coordonnées 3D
        frame_number: Numéro de la frame actuelle
    
    Returns:
        Dictionnaire formaté pour Blender
    """
    blender_data = {
        "frame": frame_number,
        "bones": {}
    }
    
    # Mapping des points MediaPipe vers les os Blender
    bone_mapping = {
        "left_shoulder": "shoulder.L",
        "right_shoulder": "shoulder.R",
        "left_elbow": "upper_arm.L",
        "right_elbow": "upper_arm.R",
        "left_wrist": "forearm.L",
        "right_wrist": "forearm.R",
        "left_hip": "thigh.L",
        "right_hip": "thigh.R",
        "left_knee": "shin.L",
        "right_knee": "shin.R",
        "left_ankle": "foot.L",
        "right_ankle": "foot.R"
    }
    
    for mediapipe_point, blender_bone in bone_mapping.items():
        if mediapipe_point in body_coordinates_3d:
            coords = body_coordinates_3d[mediapipe_point]
            blender_data["bones"][blender_bone] = {
                "location": [coords["x"], coords["z"], -coords["y"]],  # Conversion Y-up vers Z-up
                "visibility": coords["visibility"]
            }
    
    return blender_data

