import cv2
import time
from cvzone.HandTrackingModule import HandDetector

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is working
if not cap.isOpened():
    print("Error: Camera not found")
    exit()

# Initialize the hand detector
detector = HandDetector(detectionCon=0.8)

# Error handling and frame capture check
error_count = 0
max_errors = 5

while True:
    # Capture the frame
    success, img = cap.read()

    # Check if the frame is captured successfully
    if not success or img is None:
        print("Error: Failed to capture frame")
        error_count += 1
        if error_count > max_errors:
            print("Too many errors, exiting...")
            break
        continue

    # Process the image
    try:
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        lmList, bboxInfo = detector.findHands(img)  # Get landmarks and bounding box info
        if lmList:
            # Do something with the landmarks (e.g., draw the bounding box or landmarks)
            pass

        # Show the processed image
        cv2.imshow("AI Virtual Keyboard", img)

    except Exception as e:
        print(f"Error during processing: {e}")
        error_count += 1
        if error_count > max_errors:
            print("Too many errors, exiting...")
            break

    # Wait for the user to press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close any open windows
cap.release()
cv2.destroyAllWindows()
