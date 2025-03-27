import cv2
import time
import glob
import os
from mailing import send_email
from threading import Thread

# Open camera
video = cv2.VideoCapture(0)

# Wait 1 second for camera to open and configure
time.sleep(1)

first_frame = None
status_list = []
count = 1

# Delete images inside images folder
def clean_folder():
    print("clean folder function started")
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
    print("clean folder function ended")

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

            # Create a single folder if that folder does not exist
            if not os.path.isdir("images"):
                os.mkdir("images")

            # Save frames where object appear as image
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1

            # Loading the image saved in the middle to a variable      
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            if len(all_images) > 0:
                image_with_object = all_images[index]
            print (index)           
   

    # Captures the status of the last 2 frames
    status_list.append(status)
    status_list = status_list[-2:]

    # If object leaves the frame the email is sent
    if status_list[0] ==  1 and status_list[1] == 0:
        # Prepare threads to send email
        email_thread = Thread(target=send_email, args=(image_with_object, ))
        email_thread.daemon = True
        
        # Prepare threads to clean folder
        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True

        # Execuring threads
        email_thread.start()
        

    cv2.imshow("video", frame)
    
    # Waits for 1 millisecond for a key press after imshow.
    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
        
clean_thread.start()