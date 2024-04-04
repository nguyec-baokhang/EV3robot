#!/usr/bin/env python3
from ev3dev2.motor import MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C ,OUTPUT_D,SpeedPercent, MoveTank, MoveDifferential, SpeedRPM
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor, GyroSensor
from ev3dev2.led import Leds
from ev3dev2.wheel import EV3Tire,Wheel
from ev3dev2.sound import Sound

import time
import math

#outputA is left motor
#outputB is right motor

#initialize wheel class
class MyWheel(Wheel):
    def __init__(self):
        Wheel.__init__(self, 68, 35) #wheel diameter is 68mm and 35mm width
        
left_wheel=OUTPUT_A
right_wheel=OUTPUT_D
med_motor=OUTPUT_B
wheel_distance=140
mdiff = MoveDifferential(left_wheel, right_wheel, MyWheel, wheel_distance)

isPicking=False

current_x=0
current_y=0
current_angle=90
def updatePos(distance):
    global current_x,current_y,current_angle
    current_x+=distance*math.cos(math.radians(current_angle))
    current_y+=distance*math.sin(math.radians(current_angle))

#Move forwards a distance (cm)
#Stop if there is an object 12.7 cm (5 inches) infront
def Forward(distance,speed=30,picking=False):
    mdiff.odometry_start() 
    mdiff.on_for_distance(SpeedRPM(-speed), distance*10, brake=True, block=False) #make sure block is False
    print("is Moving")
    
    while mdiff.is_running:
        print("distance in front: ",obstacle_detect())
        if not picking and obstacle_detect()<=22.7: #and not isPicking
            print("stop")
            break
        
    mdiff.stop()
    mdiff.odometry_stop()
    updatePos(distance)
    time.sleep(0.5)
    return

  
#Move backwards a distance (cm)  
def Reverse(distance):
    mdiff.on_for_distance(SpeedRPM(30),distance*10)
    updatePos(-distance)
    time.sleep(0.5)

def clamp_angle(angle_deg):
    angle_deg = angle_deg + 360.0
    mapped_angle = angle_deg % 360.0
    return mapped_angle

#Rotate counter clock wise an angle (degree)
def Rotate_CCW(angle):
    global current_x,current_y,current_angle
    
    mdiff.odometry_start(theta_degrees_start=0) 
    mdiff.turn_degrees(SpeedRPM(20),(angle),brake=True)
    mdiff.odometry_stop()
    
    current_angle+=angle
    current_angle=clamp_angle(current_angle)
    time.sleep(0.5)
    print('rotated angle:'+str(angle))
 
def obstacle_detect():
    us = UltrasonicSensor(INPUT_3)
    distance = us.distance_centimeters
    return distance

#1 is up
#-1 is down  
def moveForklift(direction):
    #if direction==1:
    #    say("picking object")
    #elif direction==-1:
    #    say("dropping object")
    medium_motor = MediumMotor(med_motor)
    medium_motor.on_for_seconds(-30*direction,5)

def say(sth):
    spkr=Sound()
    spkr.speak(sth)
#read color sensor in general 
LEFT_COLOR_SENSOR=INPUT_4
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
    if not color==1 and not color==6:
        return not_bnw
    else:
        if color==1:
            spkr= Sound()
            spkr.speak("Black")
            return black
        else:
            spkr= Sound()
            spkr.speak("White")
            return white
        
barcodes=[  [[black,white,white,white],1],      #type 1
            [[black,white,black,white],2],      #type 2
            [[black,black,white,white],3],      #type 3
            [[black,white,white,black],4]]      #type 4

def readBarcode(input=RIGHT_COLOR_SENSOR):
    barcode_read=[]
    color=readBnW(input)
    if (not color==not_bnw):
        for i in range(4):
            color=readBnW(input)
            barcode_read.append(color)
            mdiff.on_for_distance(SpeedRPM(-10), 1.27*10, brake=True, block=True)
    print(barcode_read)
    bc_type=getBarcodeType(barcode_read)
    return bc_type

def getBarcodeType(bc):
    code=-1
    if not len(bc)== 4:
        bc=[not_bnw,not_bnw,not_bnw,not_bnw]
    for i in range(0,len(barcodes)):
        found = True
        for j in range(4):
            if not (bc[j] ==barcodes[i][0][j]):
                found=False
                break
        if (found):
            code=barcodes[i][1]
            print('found ', str(code))
            return code
    return -1
    
def moveToXY(new_x,new_y):
    global current_x,current_y,current_angle
    if (current_x!=0):
        Rotate_CCW(180-current_angle)
        Forward(current_x)
    if (new_y>current_y):
        Rotate_CCW(90-current_angle)
        Forward(new_y-current_y)
    elif (new_y<current_y):
        Rotate_CCW(270-current_angle)
        Forward(current_y-new_y)
    
    Rotate_CCW(-current_angle)
    Forward(new_x-current_x)

#Forward(200)
#code=-1
#while code==-1:
#    code=readBarcode(LEFT_COLOR_SENSOR)
#    #print(code)
#    #print(readBnW(RIGHT_COLOR_SENSOR))
#spkr= Sound()
#sent="found code "+str(code)
#spkr.speak(sent)

#Rotate_CCW(90)
#Rotate_CCW(-90)
#Rotate_CCW(90)
#Rotate_CCW(-90)
#Rotate_CCW(90)
#Rotate_CCW(-90)
moveForklift(-1)
moveToXY(50,100)
Rotate_CCW(-90-current_angle)
obj_dist=obstacle_detect()
obj_dist-=6.0
if obj_dist>50 or obj_dist<=0.0:
    obj_dist=0
Forward(obj_dist,picking=True)
moveForklift(1)
Reverse(obj_dist)
moveToXY(0,0)
