#!/usr/bin/env python3
from ev3dev2.motor import MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C ,OUTPUT_D,SpeedPercent, MoveTank, MoveDifferential, SpeedRPM
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor
from ev3dev2.led import Leds
from ev3dev2.wheel import EV3Tire,Wheel
import time
import os
import numpy as np

#outputA is left motor
#outputB is right motor

#initialize wheel class
class MyWheel(Wheel):
    def __init__(self):
        Wheel.__init__(self, 68, 35) #wheel diameter is 68mm and 35mm width
        
left_wheel=OUTPUT_A
right_wheel=OUTPUT_D
med_motor=OUTPUT_B
wheel_distance=143
mdiff = MoveDifferential(left_wheel, right_wheel, MyWheel, wheel_distance)

isPicking=False

#Move forwards a distance (cm)
#Stop if there is an object 12.7 cm (5 inches) infront
def Forward(distance):
    #dist_moved=0.0
    #step=0.5
    #while dist_moved>=distance or (obstacle_detect()>12.7 and not isPicking):
    #    mdiff.on_for_distance(SpeedRPM(-30),step*10)
    #    dist_moved+=step
    
    mdiff.odometry_start(theta_degrees_start=90.0,x_pos_start=0.0,y_pos_start=0.0) 
    mdiff.on_to_coordinates(SpeedRPM(-30), 0, distance*10, brake=True, block=False) #make sure block is False
    print("is Moving")
    
    while mdiff.y<distance*10:
        print("distance in front: ",obstacle_detect())
        if obstacle_detect()<=12.7:
            mdiff.odometry_stop()
            return
        
    mdiff.wait()
    mdiff.odometry_stop()
    return
    
  
#Move backwards a distance (cm)  
def Reverse(distance):
    mdiff.on_for_distance(SpeedRPM(30),distance*10)

#Rotate counter clock wise an angle (degree)
def Rotate_CCW(a):
    mdiff.odometry_start(theta_degrees_start=0.0)
    mdiff.turn_degrees(SpeedRPM(30),(a))
    mdiff.odometry_stop()
    angle+=a
def obstacle_detect():
    us = UltrasonicSensor()
    distance = us.distance_centimeters
    return distance

#not finished for forklift !!!!!    
def moveMed(sth):
    medium_motor = MediumMotor(med_motor)
    medium_motor.on_for_seconds(-30,5)

#read color sensor in general 
LEFT_COLOR_SENSOR=INPUT_4
RIGHT_COLOR_SENSOR=INPUT_2
def readColor(input=RIGHT_COLOR_SENSOR):
    col_s= ColorSensor(input)
    color=col_s.color
    #print(color)
    return color

white=0
black=1
not_bnw=2
#read only black and white color
def readBnW(input=RIGHT_COLOR_SENSOR):
    color=readColor(input)
    if not color==1 and not color==6:
        return not_bnw
    else:
        if color==1:
            return black
        else:
            return white
        
barcodes=[  [[black,white,white,white],1],      #type 1
            [[black,white,black,white],2],      #type 2
            [[black,black,white,white],3],      #type 3
            [[black,white,white,black],4]]      #type 4

shelf = [[[12,12],"A1"],       #A1 shelf
         [[12,36],"A2"],       #A2 shelf
         [[60,12],"B1"],       #B1 shelf
         [[60,36],"B2"],       #B2 shelf
         [[12,60],"C1"],       #C1 shelf
         [[12,84],"C2"],       #C2 shelf
         [[60,60],"D1"],       #D1 shelf
         [[60,84],"D2"]]       #D2 shelf

cp = [6,-6]
angle = 90

print(shelf[1][1])
shelf_choice = input("Input the shelf: ")
def moving_to_shelf(shelf_choice):
    for i in range (len(shelf)):
        if shelf_choice == shelf[i][1]: 
            distance_y = (shelf[i][0][1]-cp[1])*2.54
            distance_x = (shelf[i][0][0]*2.54-cp[0])*2.54
            Forward(distance_y)
            Rotate_CCW(90)
            Forward(distance_x)
            cp[0] = shelf[i][0][0] 
            cp[1] = shelf[i][0][1]
            print(distance_x)
            print(distance_y)


moving_to_shelf(shelf_choice)

