import cv2
import streamlit as st
import numpy as np
import tempfile


cap = cv2.VideoCapture(1)

st.title("SINWicHacks25")

frame_placeholder = st.empty()

stop_button_pressed = st.button("Stop")
start_button_pressed = st.button("Start")

while start_button_pressed:

    while cap.isOpened() and not stop_button_pressed:
        ret, frame = cap.read()

        if not ret:
            st.write("The webcam is not accessible")
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = frame[:, ::-1,:]

        frame_placeholder.image(frame, channels="RGB")

        if (cv2.waitKey(1) & 0xFF == ord('q')) or stop_button_pressed:
            break
    while stop_button_pressed:
        cap.release()
        cv2.destroyAllWindows()
