
import numpy as np 
import time 
import cv2
import handTracking as ht
import math
from subprocess import call
##### defining cam width and height ######
wCam,hCam = 640,640
detector = ht.handDetector(detectionCon=0.6)
cap = cv2.VideoCapture(0)
# print(cap.get(3),cap.get(4))
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
while True:
    success,img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    if len(lmList) !=0 :
        x1,y1 = lmList[4][1],lmList[4][2]
        x2,y2 = lmList[8][1],lmList[8][2]
        cx,cy = (x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(x1,y1),15,(255,0,0),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,0),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)
        cv2.circle(img,(cx,cy),15,(255,0,0),cv2.FILLED)
        length = math.hypot(x2-x1,y2-y1)
        val = int((length*100)/290)
        print(length)
        call(["amixer", "-D", "pulse", "sset", "Master", f"{val}%"])

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime 
    cv2.putText(img,f'FPS: {int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
    cv2.imshow("Img",img)
    cv2.waitKey(1)