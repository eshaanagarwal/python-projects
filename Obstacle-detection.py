from controller import Robot, Motor, DistanceSensor,Camera
import numpy as np
import math
import cv2

robot = Robot()
camera=robot.getDevice('camera')
camera.enable(1)
timestep = int(robot.getBasicTimeStep())

left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')

left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0)
right_motor.setVelocity(0)   

max_speed=6.28

setspeed=0.5*max_speed

ps=[]
for i in range(8):
    name= 'ps' +str(i)
    ps.append(robot.getDevice(name))
    ps[i].enable(timestep)     



def moveForward(speed):
    if(speed>100):
        speed = 100
    speed = (max_speed/100.0)*speed
    for i in range(10):
        left_motor.setVelocity(speed)
        right_motor.setVelocity(speed)

def turnRight(speed):
    if(speed>100):
        speed = 100
    speed = (max_speed/100.0)*speed
    for i in range(10):
        left_motor.setVelocity(speed)
        right_motor.setVelocity(-speed)

def stop():
    left_motor.setVelocity(0)
    right_motor.setVelocity(0) 
    
def rotate():
    left_motor.setVelocity(6.28)
    right_motor.setVelocity(0)
            
def turnLeft(speed):
    if(speed>100):
        speed = 100
    speed = (max_speed/100.0)*speed
    for i in range(10):
        left_motor.setVelocity(-speed)
        right_motor.setVelocity(speed)

def frontIrReading():
    return math.floor(ps[0].getValue()+ps[7].getValue())
    
def leftIrReading():
    return math.floor(ps[5].getValue())
    
def rightIrReading():
    return math.floor(ps[2].getValue())    
        
target=1                
while robot.step(timestep) != -1:   
    
    
    camera.saveImage('rgb.jpg',100)
    rgb=cv2.imread('rgb.jpg')
    cv2.imshow('original',rgb)
    img=cv2.cvtColor(rgb,cv2.COLOR_BGR2HSV)
    H,W,C=img.shape
    rotate()
    
    if(target==1):
          lower_color =np.array([55,38,38])
          upper_color =np.array([97,253,255])
    if(target==2):
          lower_color =np.array([115,90,90])
          upper_color =np.array([135,255,255])
    if(target==3):
          lower_color =np.array([135,55,45])
          upper_color =np.array([162,253,255])  
    if(target==4):
        lower_color =np.array([162,48,51])
        upper_color =np.array([255,255,255])
        
    # rgb=cv2.medianBlur(rgb,5)

    mask_color=cv2.inRange(img,lower_color,upper_color)
    # det_color=cv2.bitwise_and(img,img,mask=mask_color)
    contours,garbage= cv2.findContours(mask_color,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.imshow('masked', mask_color)
    cv2.waitKey(1)
    if(len(contours)>=1):
         contours=sorted(contours,key=lambda x:cv2.contourArea(x),reverse=True)
         if(target==4):
             per=0.78
             
         else:
             per=0.9
         if(cv2.contourArea(contours[0])>per*H*W):
             
      
             target+=1
             if(target==5):
                 print("Hey Vision! I Rescued You!!")
                 for i in range(50000):
                     left_motor.setVelocity(6)
                     right_motor.setVelocity(6) 
                 for i in range(20):
                     left_motor.setVelocity(0)
                     right_motor.setVelocity(0)
                 break
             for i in range(20):
                 left_motor.setVelocity(-6.28)
                 right_motor.setVelocity(-6.28)
                 robot.step(timestep)
         elif(cv2.contourArea(contours[0])>500):
             L=cv2.moments(contours[0])
             if(L['m00']!=0) :
                   cx=int(L['m10']/L['m00'])
                   cy=int(L['m01']/L['m00'])
                   print(cx,cy,cv2.contourArea(contours[0]),len(contours))
                   print(ps[0].getValue()+ps[7].getValue())
                   
             
             if(cx>200 and cx<312):
                 moveForward(80)
             elif(cx<200):
                 turnLeft(80)
             else:
                 turnRight(80)
    print(target)
      
    pass
    
