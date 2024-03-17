#!/usr/local/bin/python3.11

import cv2

#def float_to_int(bbox):
#    x = int(bbox[0])
#    y = int(bbox[1])
#    w = int(bbox[2])
#    h = int(bbox[3])
#    return (x, y, w, h)

def calculate_iou(bbox1, bbox2):
    # Calculate intersection rectangle
    x1 = max(bbox1[0], bbox2[0])
    y1 = max(bbox1[1], bbox2[1])
    x2 = min(bbox1[0] + bbox1[2], bbox2[0] + bbox2[2])
    y2 = min(bbox1[1] + bbox1[3], bbox2[1] + bbox2[3])

    # Calculate area of intersection rectangle
    inter_area = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)
       
    # Calculate area of both bounding boxes
    bbox1_area = (bbox1[2] + 1) * (bbox1[3] + 1)
    bbox2_area = (bbox2[2] + 1) * (bbox2[3] + 1)
            
    # Calculate IoU
    iou = inter_area / float(bbox1_area + bbox2_area - inter_area)
    return iou

def evaluate_stability(video_path, ground_truth_bboxes, interval=50):

    # Open the video capture object
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video file")
        return

    iou_values = []
    frame_count = 0

    tracker = cv2.TrackerCSRT_create()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read first frame")
            break

        # Get the ground truth bounding box for the current frame
        if frame_count < len(ground_truth_bboxes):
            ground_truth_bbox = ground_truth_bboxes[frame_count]
        else:
            # Extend the ground truth bounding boxes to cover all frames
            ground_truth_bbox = ground_truth_bboxes[-1]


        # Initialize the tracker with the first frame and ground truth bounding box
        if frame_count == 0:
            tracker.init(frame, ground_truth_bbox)

        # Get the tracked bounding box for the current frame
        success, tracked_bbox = tracker.update(frame)

        if success:

            # Calculate IoU between ground truth and tracked bounding boxes
            iou = calculate_iou(ground_truth_bbox, tracked_bbox)
            iou_values.append(iou)

        # Check if it's time to evaluate stability
        if frame_count % interval == 1:
            avg_iou = sum(iou_values) / len(iou_values)
            print(f"Average IoU at frame {frame_count}: {avg_iou}")

        # Increment frame count
        frame_count += 1

    # Release resources
    cap.release()

# Test the tracking evaluation
if __name__ == "__main__":
    # Provide the path to the video file
    video_path = "video_test.mp4"
    
    # Manually annotate ground truth bounding boxes for each frame
    ground_truth_bboxes = []
    for i in range(300):
        start = 331
        step = int(-2.01*i)
        ground_truth_bboxes += [(750, start + step, 67, 129)]
    #print(ground_truth_bboxes)

    # Evaluate tracking performance
    evaluate_stability(video_path, ground_truth_bboxes)

