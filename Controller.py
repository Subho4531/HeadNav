import cv2
import mediapipe as mp
import pyautogui


mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cv2.setNumThreads(8)

# Set up camera 
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FPS, 120)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)


screen_width, screen_height = pyautogui.size()


initial_x, initial_y = None, None
sensitivity = 2000 # Control the sensivity
dead_zone = 0.02 
smoothing_factor = 0.99 


smoothed_x, smoothed_y = 0, 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    frame = cv2.flip(frame, 1) 
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    
    face_result = face_mesh.process(rgb_frame)

    if face_result.multi_face_landmarks:
        for face_landmarks in face_result.multi_face_landmarks:
            
            nose_tip = face_landmarks.landmark[1]
            current_x = nose_tip.x
            current_y = nose_tip.y

            if initial_x is None or initial_y is None:
               
                initial_x, initial_y = current_x, current_y

            
            delta_x = current_x - initial_x
            delta_y = current_y - initial_y

           
            if abs(delta_x) > dead_zone or abs(delta_y) > dead_zone:
                smoothed_x = smoothing_factor * smoothed_x + (1 - smoothing_factor) * delta_x
                smoothed_y = smoothing_factor * smoothed_y + (1 - smoothing_factor) * delta_y

                
                move_x = smoothed_x * sensitivity
                move_y = smoothed_y * sensitivity

               
                mouse_x, mouse_y = pyautogui.position()

               
                new_x = min(max(mouse_x + move_x, 0), screen_width - 1)
                new_y = min(max(mouse_y + move_y, 0), screen_height - 1)
                pyautogui.moveTo(new_x, new_y, duration=0)
            else:
                
                smoothed_x, smoothed_y = 0, 0

            cv2.putText(
                frame,
                f"Delta: ({delta_x:.3f}, {delta_y:.3f})",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

    # Display the video feed
    cv2.imshow("Head Tracking Mouse Control", frame)

    # Quit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
