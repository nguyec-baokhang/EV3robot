#!/usr/bin/env python3
from ev3dev2.motor import MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C ,OUTPUT_D,SpeedPercent, MoveTank, MoveDifferential, SpeedRPM
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor
from ev3dev2.led import Leds
from ev3dev2.wheel import EV3Tire,Wheel
from ev3dev2.sound import Sound

import time
import os

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
    mdiff.odometry_start() 
    mdiff.on_for_distance(SpeedRPM(-30), distance*10, brake=True, block=False) #make sure block is False
    print("is Moving")
    
    while mdiff.is_running:
        print("distance in front: ",obstacle_detect())
        if obstacle_detect()<=12.7:
            print("stop")
            break
        
    mdiff.stop()
    mdiff.odometry_stop()
    return
    
  
#Move backwards a distance (cm)  
def Reverse(distance):
    mdiff.on_for_distance(SpeedRPM(30),distance*10)

#Rotate counter clock wise an angle (degree)
def Rotate_CCW(angle):
    mdiff.odometry_start(theta_degrees_start=0.0)
    mdiff.turn_degrees(SpeedRPM(30),(angle))
    mdiff.odometry_stop()
 
def obstacle_detect():
    us = UltrasonicSensor(INPUT_3)
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

Forward(200)