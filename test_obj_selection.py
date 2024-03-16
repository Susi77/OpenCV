#!/usr/local/bin/python3.11
import cv2


def test_object_selection():

    # Define the video file path or 0 for webcam input

    video_path = "video_test1.mp4" 

    # Open the video capture object

    cap = cv2.VideoCapture(video_path)


    if not cap.isOpened():

        print("Error: Could not open video file")
        return
    
    # Read the first frame

    ret, frame = cap.read()

    
    if not ret:

        print("Error: Could not read first frame")
        cap.release()
        return
    
    # Use selectROI to select the object

    bbox = cv2.selectROI("Test Object Selection", frame)

    # Close the window after selecting the ROI

    cv2.destroyWindow("Test Object Selection")

    # Check if a bounding box was selected

    if bbox == (0, 0, 0, 0):
        print("Test Failed: No bounding box selected")
    else:
        print("Test Passed: Bounding box selected successfully")

    # Release resources
    cap.release()

# Run the test case 
test_object_selection()
