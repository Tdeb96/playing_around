#import keras
from fer import FER
import cv2
import numpy as np
import matplotlib
import cv2
import numpy as np
import random
import time
import os

emotion_detector = FER()

# Our sketch generating function


def get_emotion(image):

    dominant_emotion, emotion_score = emotion_detector.top_emotion(image)

    return [dominant_emotion, emotion_score]


def get_objective_emotion():
    emotions = ['happy', 'sad', 'fear',
                'disgust', 'angry', 'neutral', 'surprise']
    return random.choice(emotions)


def show_frame(frame, emotion, score, target_emotion):

    # Initialize text settings

    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    fontColor = (255, 255, 255)
    thickness = 1
    lineType = 2

    # add detected emotion to the frame
    cv2.putText(frame, f"""Detected emotion: {emotion[0]}""",
                (10, 500),
                font,
                fontScale,
                fontColor,
                thickness,
                lineType)
    cv2.putText(frame, f"""Emotion score: {str(get_emotion(frame)[1])}""",
                (10, 550),
                font,
                fontScale,
                fontColor,
                thickness,
                lineType)

    cv2.putText(frame, f"""Score: {str(score)}""",
                (10, 100),
                font,
                fontScale,
                fontColor,
                thickness,
                lineType)
    cv2.putText(frame, f"""Target emotion : {target_emotion}""",
                (10, 150),
                font,
                fontScale,
                fontColor,
                thickness,
                lineType)

    # display the frame
    cv2.imshow('game of emotions', (frame))

    # Initialize video capture object
cap = cv2.VideoCapture(0)

# initialize tracking variables
score = 0
target_emotion = None
start_time = time.time()
idle_time = 10

while True:

    loop_time = time.time()

    # capture the frame and detect the emotion
    ret, frame = cap.read()
    detected_emotion = get_emotion(frame)

    if (idle_time != 0) and (loop_time-start_time < idle_time) and (target_emotion is None):
        show_frame(frame, detected_emotion, score, target_emotion)
        continue
    elif (idle_time != 0) and (loop_time-start_time >= idle_time) and (target_emotion is None):
        idle_time = 0
        start_time = time.time()

    # get new target_emotion if none
    if target_emotion is None:
        target_emotion = get_objective_emotion()
        print(target_emotion)
        idle_time = 2
        start_time = time.time()
        show_frame(frame, detected_emotion, score, target_emotion)
        continue

    # detect the emotion and check if equal to objective emotion
    if (detected_emotion[0] == target_emotion) and (detected_emotion[1] > 0.8):
        print("Success!")
        target_emotion = None
        idle_time = 5
        start_time = time.time()
        score += 1
        print("Score: ", score)

    show_frame(frame, detected_emotion, score, target_emotion)

    if cv2.waitKey(1) == 13:  # 13 is the Enter Key
        break

# Release camera and close windows
cap.release()
cv2.destroyAllWindows()
