import cv2
import numpy as np
import time

# Define the path to the video file
video_path = 'timelapses/newcastlegate06_multi_test01_0.2mm_PLA_MK3SMMU2S_1d20h42m_20220509072520.mp4'

# Create a VideoCapture object to read the video
cap = cv2.VideoCapture(video_path)

# Get the frames per second (fps) and frame size of the video
fps = cap.get(cv2.CAP_PROP_FPS)
frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

# Define a function to convert an RGB frame to grayscale
def to_grayscale(frame):
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Convert the grayscale frame back to RGB so we can display it
    processed_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)
    return processed_frame

# Initialize the previous frame to None
prev_frame = None
output_frames = []

# Loop through each frame in the video
while cap.isOpened():
    # Read the frame from the video
    ret, frame = cap.read()
    # If we reached the end of the video, break the loop
    if not ret:
        break

    # Convert the current frame to grayscale
    gray_frame = to_grayscale(frame)
    # Subtract the current frame from the previous frame
    if prev_frame is not None:
        diff_frame = cv2.subtract(gray_frame, prev_frame)
    else:
        diff_frame = np.zeros_like(frame)
    prev_frame = gray_frame

    # Concatenate the original frame and the difference frame horizontally
    output_frame = np.concatenate((frame, diff_frame), axis=1)
    output_frames.append(output_frame)

cv2.namedWindow('Video', cv2.WINDOW_NORMAL)

# Initialize the current frame index
frame_idx = 0
while True:
    output_frame = output_frames[frame_idx]
    # Display the processed frame
    cv2.imshow('Video', output_frame)

    key = cv2.waitKey()
    # Check if the user pressed the 'q' key to exit
    if key & 0xFF == ord('q'):
        break
    # Check if the user pressed the right arrow key to advance 1 frame
    elif key == 3: # right arrow key
        frame_idx += 1
    # Check if the user pressed the left arrow key to rewind 1 frame
    elif key == 2: # left arrow key
        frame_idx -= 1

# Release the VideoCapture object and close the window
cap.release()
cv2.destroyAllWindows()

