import cv2
import mediapipe as mp

# Face Mesh
mp_face_mesh = mp.solutions.face_mesh
mp_face_mesh = mp_face_mesh.FaceMesh()

cap = cv2.VideoCapture(0)

while True:
    # Image
    ret, image = cap.read()
    if not ret:
        print("Ignoring empty camera frame.")
        continue
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Facial Landmarks
    result = mp_face_mesh.process(image)

    for facial_landmarks in result.multi_face_landmarks:
        for i in range(len(facial_landmarks.landmark)):
            x = facial_landmarks.landmark[i].x
            y = facial_landmarks.landmark[i].y
            z = facial_landmarks.landmark[i].z
            print(f'{i} - X: {x}, Y: {y}, Z: {z}')

            cv2.circle(image, (int(x * image.shape[1]), int(y * image.shape[0])), 1, (0, 0, 255), 1)  



    cv2.imshow('Image', image)
    cv2.waitKey(1)