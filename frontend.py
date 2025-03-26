import cv2
import streamlit as st
import time

st.title("Motion Detector")
start = st.button("Start Camera")


if start:

    streamlit_image = st.image([])
    camera = cv2.VideoCapture(0)

    while True:
        local_time = time.localtime()

        current_date = time.strftime('%Y-%m-%d', local_time)
        current_time = time.strftime('%H:%M:%S', local_time)
        check, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        cv2.putText(img=frame, text=current_date, org=(20,30),
            fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2,
            color=(100, 100, 100), thickness=2, 
            lineType=cv2.LINE_AA)
        
        cv2.putText(img=frame, text=current_time, org=(20,60),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2,
                    color=(20, 100, 200), thickness=2, 
                    lineType=cv2.LINE_AA)
        
        streamlit_image.image(frame)