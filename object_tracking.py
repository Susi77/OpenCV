#!/usr/local/bin/python3.11

import cv2

def float_to_int(bbox):
    x = int(bbox[0])
    y = int(bbox[1])
    w = int(bbox[2])
    h = int(bbox[3])
    return (x, y, w, h)


# Define the video file path or 0 for webcamera input
video_path = "video_test1.mp4" 

# Open the video capture object
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video file")
    exit()

# Read the first frame
ret, frame = cap.read()

if not ret:
    print("Error: Could not read first frame")
    exit()

# Use selectROI(region of interest) to select the object
bbox = cv2.selectROI("Select object", frame)

# Close the window after selecting the ROI
cv2.destroyWindow("Select object")

# Create the CSRT(Discriminative Correlation Filter with Channel and Spatial Reliability) tracker
tracker = cv2.TrackerCSRT_create()

# Initialize the tracker with the bounding box
tracker.init(frame, bbox)

while True:
    # Read the next frame
    ret, frame = cap.read()

    # Check if frame is read successfully
    if not ret:
        print("No more frames to read")
        break

    # Update the tracker with the current frame
    success, bbox = tracker.update(frame)

    # Draw the bounding box on the frame
    if success:
        x, y, w, h = float_to_int(bbox)  # Extract coordinates, width, and height from the bounding box
        # Calculate centroid
        centroid_x = x + w // 2
        centroid_y = y + h // 2
        # Draw cross at centroid
        cross_size = 10
        cv2.line(frame, (centroid_x - cross_size, centroid_y), (centroid_x + cross_size, centroid_y), (0, 0, 255), 1)
        cv2.line(frame, (centroid_x, centroid_y - cross_size), (centroid_x, centroid_y + cross_size), (0, 0, 255), 1)

    # Display the resulting frame
    cv2.imshow('Tracking', frame)

    # Exit the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

print("Tracking complete!")

# cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)  # Draw rectangle using all four arguments
