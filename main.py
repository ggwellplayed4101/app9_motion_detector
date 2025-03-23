import cv2
import time

# Open camera
video = cv2.VideoCapture(0)

# Wait 1 second for camera to open and configure
time.sleep(1)

first_frame = None

# Continuosly read frames
while True:
    # Frame stores the image data in matrix form
    check, frame = video.read()

    """ Apply gray scale and Gausian blur 
    To Make the matrix less complex """
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21,21), 0)


    # Record first frame
    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # Convert grayscale video to white and black
    thresh_frame = cv2.threshold(delta_frame, 40, 255, 
                                 cv2.THRESH_BINARY)[1]
    
    # Fill the hole in whitespace
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    cv2.imshow("My video", dil_frame)

    key = cv2.waitKey(1)

    # Find outlines of the image
    contours, check = cv2.findContours(dil_frame, 
                                       cv2.RETR_EXTERNAL, 
                                       cv2.CHAIN_APPROX_SIMPLE)

    if key == ord("q"):
        break

video.release()