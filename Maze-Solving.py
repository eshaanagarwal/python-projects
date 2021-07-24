from controller import Robot, Motor, DistanceSensor
import numpy as np
import math

robot = Robot()

timestep = 1

left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')

left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
max_speed=6.27

setspeed=0.5*max_speed

ps=[]
for i in range(8):
    name= 'ps' +str(i)
    ps.append(robot.getDevice(name))
    ps[i].enable(timestep)     
    
        
                
while robot.step(timestep) != -1:   
    
    
    
    
    right_wall = ps[2].getValue() > 80 and ps[1].getValue()>80
    left_wall = ps[5].getValue() > 80  and ps[6].getValue()>80
    front_wall = ps[0].getValue()+ps[7].getValue() > 180
    
    
    left_speed = max_speed
    right_speed = max_speed
    print(right_wall,front_wall,left_wall)  
    if right_wall and left_wall:
        print("Forward")
        left_speed = max_speed/2.0
        right_speed = max_speed/2.0
        
    elif right_wall and front_wall:
        print("Left")
        left_speed = -max_speed/14.0
        right_speed = max_speed/2.0
        
    elif front_wall:
           print("Right")
           left_speed = max_speed/2.0
           right_speed = -max_speed/14.0
        
       
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)
    
        
    pass