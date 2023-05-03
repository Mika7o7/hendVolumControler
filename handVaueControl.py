import cv2
import time
import numpy as np
import handTrackingModule as htm
import math
from subprocess import call

################################
wCam, hCam = 640, 480
################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector()





while True:
    succss, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) !=0:
        


        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2)//2, (y1+ y2)//2


        cv2.circle(img, (x1, y1), 7, (255,0,0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 7, (255,0,0), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,0), 3)
        cv2.circle(img, (cx, cy), 7, (255,0,0), cv2.FILLED)

        volume = math.hypot(x2 - x1, y2 - y1)
        

        

        if volume < 50:
            cv2.circle(img, (cx, cy), 7, (0,255,0), cv2.FILLED)



        try:
            volume = int(volume)

            if (volume <= 100) and (volume >= 0):
                call(["amixer", "-D", "pulse", "sset", "Master", str(volume)+"%"])
                valid = True

        except ValueError:
            pass

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f"FPS: {int(fps)}", (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)


    cv2.imshow('img', img)
    cv2.waitKey(1)