#!/usr/bin/env python3
from ev3dev2.motor import MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C ,OUTPUT_D,SpeedPercent, MoveTank, MoveDifferential, SpeedRPM
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.led import Leds
from ev3dev2.wheel import EV3Tire,Wheel
import time


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

#Move forwards a distance (cm)
def Forward(distance):
    mdiff.on_for_distance(SpeedRPM(-30),distance*10)
  
#Move backwards a distance (cm)  
def Reverse(distance):
    mdiff.on_for_distance(SpeedRPM(30),distance*10)

#Rotate counter clock wise an angle (degree)
def Rotate_CCW(angle):
   
    mdiff.odometry_start(theta_degrees_start=0.0)
    mdiff.turn_degrees(SpeedRPM(30),(angle))
    mdiff.odometry_stop()
 
#not finished for forklift !!!!!    
def moveMed(sth):
    medium_motor = MediumMotor(med_motor)
    medium_motor.on_for_seconds(-30,5)

#read color sensor in general 
LEFT_COLOR_SENSOR=INPUT_1
RIGHT_COLOR_SENSOR=INPUT_2
def readColor(input=RIGHT_COLOR_SENSOR):
    col_s= ColorSensor(input)
    color=col_s.color
    print(color)
    return color

white=0
black=1
not_bnw=2
#read only black and white color
def readBnW(input=RIGHT_COLOR_SENSOR):
    color=readColor(input)
    if not color==1 or not color==6:
        return not_bnw
    else:
        if color==1:
            return black
        else:
            return white
        
barcodes=[  [black,white,white,white],      #type 1
            [black,white,black,white],      #type 2
            [black,black,white,white],      #type 3
            [black,white,white,black]]      #type 4

while True:
    print(readBnW(RIGHT_COLOR_SENSOR))        