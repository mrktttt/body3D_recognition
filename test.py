import cv2
import mediapipe as mp

cv2.namedWindow("Détection du squelette", cv2.WINDOW_NORMAL)
cv2.startWindowThread()

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

cap = cv2.VideoCapture(0)

with pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Erreur lecture webcam")
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow("Détection du squelette", image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)


# Fonction pour dessiner seulement certains landmarks
def draw_selected_landmarks(image, landmarks, connections, selected_indices):
    # Dessiner uniquement les landmarks sélectionnés
    for idx, landmark in enumerate(landmarks.landmark):
        if idx in selected_indices:
            h, w, c = image.shape
            cx, cy = int(landmark.x * w), int(landmark.y * h)
            cv2.circle(image, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
    
    # Dessiner les connections entre les landmarks sélectionnés
    for connection in connections:
        if connection[0] in selected_indices and connection[1] in selected_indices:
            start_idx, end_idx = connection
            start_landmark = landmarks.landmark[start_idx]
            end_landmark = landmarks.landmark[end_idx]
            
            h, w, c = image.shape
            start_point = (int(start_landmark.x * w), int(start_landmark.y * h))
            end_point = (int(end_landmark.x * w), int(end_landmark.y * h))
            
            cv2.line(image, start_point, end_point, (0, 255, 0), 2)

# Exemple: sélectionner uniquement les landmarks des bras
# Vous pouvez ajuster cette liste selon vos besoins
# Voir https://developers.google.com/mediapipe/solutions/vision/pose_landmarker pour les indices
selected_landmarks = [
    # Épaules
    11, 12,
    # Coudes
    13, 14,
    # Poignets
    15, 16
]