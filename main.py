import cv2
import mediapipe as mp
import time

# Initialize MediaPipe Hands and Camera
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set the camera width
cap.set(4, 720)   # Set the camera height

# Keyboard Layout
keys = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
    ['z', 'x', 'c', 'v', 'b', 'n', 'm']
]

# Define key dimensions
key_width = 90
key_height = 90
key_margin = 15

# Create a dictionary to store the key bounding box positions
key_boxes = {}

# Function to draw keys on the screen
def draw_keys(img):
    y_offset = 50  # Vertical offset for the first row of keys

    for row in range(len(keys)):
        x_offset = 50  # Horizontal offset for each key in the row
        for col in range(len(keys[row])):
            key = keys[row][col]
            x1, y1 = x_offset, y_offset
            x2, y2 = x_offset + key_width, y_offset + key_height
            key_boxes[key] = (x1, y1, x2, y2)
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.putText(img, key, (x1 + 35, y1 + 65), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            x_offset += key_width + key_margin
        y_offset += key_height + key_margin

# Function to detect keypress based on finger position
def detect_key(lmList):
    if lmList:
        # Get the index finger tip position (landmark 8)
        x, y = lmList[8]  # Index finger tip
        # Map the position to the keyboard area
        for key, (x1, y1, x2, y2) in key_boxes.items():
            if x1 < x < x2 and y1 < y < y2:
                return key
    return None

# Main loop for hand tracking and virtual keyboard
while True:
    success, img = cap.read()
    if not success:
        break

    # Convert image to RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Get hand landmarks
    results = hands.process(imgRGB)

    # Draw keyboard on the screen
    draw_keys(img)

    # If hand landmarks are found, draw them and detect key press
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the landmarks as a list
            lmList = [(lm.x * img.shape[1], lm.y * img.shape[0]) for lm in hand_landmarks.landmark]

            # Detect keypress based on the index finger position
            key = detect_key(lmList)

            if key:
                # Display the detected key on the screen
                cv2.putText(img, f"Pressed: {key}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                print(f"Key Pressed: {key}")

    # Show the image with the drawn keyboard and hand landmarks
    cv2.imshow("Virtual Keyboard", img)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()



