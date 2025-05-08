import cv2

# Open the default camera (index 0)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    flipped_frame = cv2.flip(frame, 1)
    if not ret:
        break

    # Display the resulting frame
    cv2.imshow('frame', flipped_frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

