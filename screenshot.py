import cv2
import mediapipe as mp
import pyautogui

# Set up Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Set up webcam
cap = cv2.VideoCapture(0)

# Initialize variables
prev_state = 0  # Previous state of hand (0 for open, 1 for closed)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and get hand landmarks
    results = hands.process(rgb_frame)

    # Check if hand is detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the state of the hand (open or closed)
            state = 0 if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].visibility > 0.7 else 1

            # If the hand state has changed to closed, take a screenshot
            if prev_state == 0 and state == 1:
                screenshot = pyautogui.screenshot()
                screenshot.save("screenshot.png")
                print("Screenshot taken!")

            # Update the previous state
            prev_state = state

    # Display the frame
    cv2.imshow('Hand Tracking', frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
