import cv2
import mediapipe as mp
import pyautogui


mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cv2.setNumThreads(8)

# Set up camera (using camera index 2)
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FPS, 120)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

# Screen dimensions for mouse movement mapping
screen_width, screen_height = pyautogui.size()

# Variables for head tracking
initial_x, initial_y = None, None
sensitivity = 2000 # Higher sensitivity for finer movements
dead_zone = 0.02  # Threshold for no movement near initial position
smoothing_factor = 0.99  # High smoothing for ultra-smooth movements

# Variables for smoothing
smoothed_x, smoothed_y = 0, 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    frame = cv2.flip(frame, 1)  # Mirror the frame
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with Mediapipe
    face_result = face_mesh.process(rgb_frame)

    if face_result.multi_face_landmarks:
        for face_landmarks in face_result.multi_face_landmarks:
            # Use nose tip (landmark 1) as reference for head position
            nose_tip = face_landmarks.landmark[1]
            current_x = nose_tip.x
            current_y = nose_tip.y

            if initial_x is None or initial_y is None:
                # Set initial position for calibration
                initial_x, initial_y = current_x, current_y

            # Calculate relative movement from initial position
            delta_x = current_x - initial_x
            delta_y = current_y - initial_y

            # Apply smoothing and check dead zone
            if abs(delta_x) > dead_zone or abs(delta_y) > dead_zone:
                smoothed_x = smoothing_factor * smoothed_x + (1 - smoothing_factor) * delta_x
                smoothed_y = smoothing_factor * smoothed_y + (1 - smoothing_factor) * delta_y

                # Scale movements for mouse control
                move_x = smoothed_x * sensitivity
                move_y = smoothed_y * sensitivity

                # Get current mouse position
                mouse_x, mouse_y = pyautogui.position()

                # Move the mouse by delta values
                new_x = min(max(mouse_x + move_x, 0), screen_width - 1)
                new_y = min(max(mouse_y + move_y, 0), screen_height - 1)
                pyautogui.moveTo(new_x, new_y, duration=0)
            else:
                # Reset smoothed values when in dead zone
                smoothed_x, smoothed_y = 0, 0

            # Optional: Display debug info
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
