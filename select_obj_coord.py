#!/usr/local/bin/python3.11

import cv2

def select_object(video_path):


    # Open the video capture object
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video file")
        return
   
    # Read the first frame
    ret, frame = cap.read()

    if not ret:
       print("Error: Could not read first frame")
       return

    # Display the first frame
    cv2.imshow("Select Object", frame)

    # Use selectROI to select the object
    bbox = cv2.selectROI("Select Object", frame)

    # Close the window after selecting the ROI
    cv2.destroyWindow("Select Object")

    print("Selected Object ROI:", bbox)

    # Release resources
    cap.release()

# Test the object selection
if __name__ == "__main__":
    video_path = "video_test.mp4"
    select_object(video_path)
