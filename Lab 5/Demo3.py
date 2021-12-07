import cv2
import time
import datetime
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
import alsaaudio
import random
from collections import deque 
import pyautogui
#import pygame

screenWidth, screenHeight = pyautogui.size()
m = alsaaudio.Mixer()
################################
wCam, hCam = screenWidth, screenHeight
################################
 
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
##pygame.init()

GameContinue= True
# cycle_icon = cv2.imread('cycle.jpg')
# hand_icon = cv2.imread('hand.jpg')

#MoleImg = pygame.image.load("moles/tile002.png")
#gameDisplay= pygame.display.set_mode((wCam,hCam));
#pygame.display.set_caption('A bit Racey')

hole_list = [(400,100),(650,100),(900,100),(400,300),(650,300),(900,300),(400,500),(650,500),(900,500)]
hole_Filled =[False for i in range(9)]


detector = htm.handDetector(detectionCon=0.7)
minVol = 0
maxVol = 100
vol = 0
volBar = 400
volPer = 0


nextime= datetime.datetime.now()
nextdeletetime= datetime.datetime.now()
timestep = datetime.timedelta(0,2)
timestepdelete = datetime.timedelta(0,4)
endtime= datetime.datetime.now()
gamelength= datetime.timedelta(0,30)

state = 0

def contact(loc_1x,loc_1y, loc_2x,loc_2y,radius1,radius2):
    distanceX= abs(loc_1x-loc_2x)
    distanceY= abs(loc_1y-loc_2y)
    distanceR= radius1+radius2
    if((distanceX*distanceX+distanceY*distanceY)<distanceR*distanceR):
        return True
    return False
def contain(loc_1x,loc_1y, x1,y1,x2,y2):
    return loc_1x>=x1&&loc_1x<=x2&&loc_1y>=y1&&loc_1y<=y2
         
score = 0
circles = deque()
circles.append([hole_list[2][0],hole_list[2][1],0,2])



while True:
    print(state)
    success, img = cap.read()
    img= cv2.flip(img, 1)
    img = detector.findHands(img)
    #img= cv2.flip(img,1)
    lmList = detector.findPosition(img, draw=False)
    # random_x = random.randint(1,600)
    # random_y = random.randint(1,450)
    
    # cv2.circle(img,(200,300), 30, (255,255,0), -1) 

    font = cv2.FONT_HERSHEY_SIMPLEX

    if state == 0:
        #cv2.putText(img,'start Game', (400,300), font, 3, (255,255,255), 2, cv2.LINE_AA)
        cv2.rectangle(img, 500,200, 800,400 (255, 255, 255), 3)


    if state == 2:
        cv2.putText(img,'Yourscore: '+str(score), (1000,200), font, 2, (255,255,255), 2, cv2.LINE_AA)

    if state == 1:

        for hole in hole_list:
            cv2.circle(img, (hole[0],hole[1]), 75, (255, 200, 200), cv2.FILLED)

        now = datetime.datetime.now()
        if now>endtime:
            state = 2
            

        nowdelete= datetime.datetime.now()
        for circle in circles:
            #print(circle)
            if circle[2] is not 1:
                cv2.circle(img, (int(circle[0]),int(circle[1])), 50, (255, 255, 0), cv2.FILLED)
                cv2.circle(img, (int(circle[0]-20),int(circle[1])-15), 10, (255,255,255),cv2.FILLED)
                cv2.circle(img, (int(circle[0]+20),int(circle[1])-15), 10, (255,255,255),cv2.FILLED)
                cv2.rectangle(img, (int(circle[0]-7),int(circle[1]-7)), (int(circle[0]+7),int(circle[1]+7)), (255, 0, 0), 3)
                cv2.rectangle(img, (int(circle[0]+20),int(circle[1]+25)), (int(circle[0]-20),int(circle[1]+25)), (255, 255, 255), 3)
                #gameDisplay.blit(MoleImg, (circle[0],circle[1]))    

        print(len(circles))

        if now.time()>nextime.time():
            print("generate next circle")
            #random_x = random.randint(1,600)
            #random_y = random.randint(1,450)
            if len(circles)<9:
                random_pos = random.randint(0,8)

                while hole_Filled[random_pos]: 
                    random_pos = random.randint(0,8)

                circles.append([hole_list[random_pos][0], hole_list[random_pos][1],0, random_pos])
                hole_Filled[random_pos]= True


            nextime= now+timestep 
        if now.time()>nextdeletetime.time():
            print("delete the target")
            hole_Filled[circles[0][3]]=False
            circles.popleft()
            nextdeletetime=now+timestepdelete

        cv2.putText(img,'Score :  ' + str(score), (500,50), font, 0.5, (255,0,0), 2, cv2.LINE_AA)


    if len(lmList) != 0:
 
        thumbX, thumbY = lmList[4][1], lmList[4][2] #thumb
        pointerX, pointerY = lmList[8][1], lmList[8][2] #pointer

        middleX, middleY = lmList[12][1], lmList[12][2]
        ringX, ringY = lmList[16][1], lmList[16][2]
        pinkyX, pinkyY = lmList[20][1], lmList[20][2]
        
        cx, cy = (thumbX + pointerX) // 2, (thumbY + pointerY) // 2

        # cv2.circle(img, (thumbX, thumbY), 15, (255, 0, 255), cv2.FILLED)
        # cv2.circle(img, (pointerX, pointerY), 15, (255, 0, 255), cv2.FILLED)
        # cv2.circle(img, (middleX, middleY), 15, (255, 0, 255), cv2.FILLED)
        # cv2.circle(img, (ringX, ringY), 15, (255, 0, 255), cv2.FILLED)
        # cv2.circle(img, (pinkyX, pinkyY), 15, (255, 0, 255), cv2.FILLED)
        # cv2.line(img, (thumbX, thumbY), (pointerX, pointerY), (255, 0, 255), 3)
        # cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
       

        #index_x = (thumbX + pointerX + middleX + ringX + pinkyX + cx) // 6
        #index_y = (thumbY + pointerY + middleY + ringY + pinkyY + cy) // 6
        index_x=thumbX
        index_y=thumbY
        cv2.circle(img, (index_x, index_y), 25, (255, 0, 255), cv2.FILLED)
        
        

        
     


        #print('location is' + str(index_x) + ' ' + str(index_y))


        len_calc = lambda x1,y1,x2,y2: math.hypot(x2 - x1, y2 - y1)
        length = len_calc(thumbX,thumbY,pointerX,pointerY)
        length1 = len_calc(pointerX,pointerY,middleX,middleY)
        length2 = len_calc(middleX, middleY, ringX, ringY)
        length3 = len_calc(ringX, ringY, pinkyX, pinkyY)
        length4 = len_calc(thumbX,thumbY, ringX, ringY)
        print(length1,length2,length3)
        condition = length>100 and length1>100 and length2<100 and length3>100 and length4<100
        if condition:
            m.setvolume(0)
            volPer = 0
            volBar = 400
            print("CONDITION")
            cv2.putText(img, 'quiet coyote!', (40, 70), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 255, 255), 3)
        else:
 
            vol = np.interp(length, [50, 300], [minVol, maxVol])
            volBar = np.interp(length, [50, 300], [400, 150])
            volPer = np.interp(length, [50, 300], [0, 100])
            m.setvolume(int(vol))

        print(int(length), vol)

 
        if length < 50:

            if state == 0:
                if contain(int(index_x),int(index_y),500,200, 800,400):
                    state=1
                    endtime=datetime.datetime.now()+gamelength
            if state == 2:
                exit()

            cv2.circle(img, (index_x, index_y), 15, (0, 255, 0), cv2.FILLED)
            for circle in circles:
                x, y = circle[0],circle[1]
                if contact(index_x,int(index_y),x,y,25,50):
                    if circle[2] != 1:
                        score += 1
                    circle[2] = 1
                    hole_Filled[circle[3]]=False

 
    # cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    # cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    # cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
    #             1, (255, 0, 0), 3)
 
 
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)
    
    cv2.imshow("Img", img)
    cv2.waitKey(1)
