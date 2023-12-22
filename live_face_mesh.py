import cv2
import mediapipe as mp

# Initialize MediaPipe Face Mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

# Access webcam
cap = cv2.VideoCapture(0)

# Define parameters (adjust as needed)
image_size = (1200, 720)
static_image_mode = False
max_num_faces = 1
confidence_threshold = 0.5

# Start video capture loop
with mp_face_mesh.FaceMesh(
    static_image_mode=static_image_mode,
    max_num_faces=max_num_faces,
    refine_landmarks=True,
    min_detection_confidence=confidence_threshold) as face_mesh:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue

    # Image preprocessing
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)

    # Extract landmark data and draw mesh
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_face_landmarks:
      for face_landmarks in results.multi_face_landmarks:

           for i in range(len(face_landmarks.landmark)):
              x = face_landmarks.landmark[i].x
              y = face_landmarks.landmark[i].y
              z = face_landmarks.landmark[i].z
              print(f'{i} - X: {x}, Y: {y}, Z: {z}') 
        
      mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())

      mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_contours_style())
      
      mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_iris_connections_style())
      
      
    # Display annotated frame
    cv2.imshow('Face Mesh', image)

    # Handle key press for termination
    if cv2.waitKey(10) & 0xFF == ord('q'):
      break

# Release resources
cap.release()
cv2.destroyAllWindows()
