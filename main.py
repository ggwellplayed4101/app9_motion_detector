import cv2
import time
import glob
from mailing import send_email

# Open camera
video = cv2.VideoCapture(0)

# Wait 1 second for camera to open and configure
time.sleep(1)

first_frame = None
status_list = []
count = 1

# Continuosly read frames
while True:
    status = 0
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

    # Find outlines of the image
    contours, check = cv2.findContours(dil_frame, 
                                       cv2.RETR_EXTERNAL, 
                                       cv2.CHAIN_APPROX_SIMPLE)

    # Check for small contours less likely to be real objects
    for contour in contours:
        if cv2.contourArea(contour) < 20000:
            continue

        # Extract the recatngle around large/real objects
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x,y), 
                                  (x+w, y+h), (0, 255, 0), 3)
        
        if rectangle.any():
            status = 1
            # Save frames where object appear as image
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1
            # Loading the image saved in the middle to a variable      
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]
           

   

    # Captures the status of the last 2 frames
    status_list.append(status)
    status_list = status_list[-2:]

    # If object leaves the frame the email is sent
    if status_list[0] ==  1 and status_list[1] == 0:
        send_email()

    cv2.imshow("video", frame)
    
    # Waits for 1 millisecond for a key press after imshow.
    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()