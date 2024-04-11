#!/usr/bin/env python3
from ev3dev2.motor import MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C ,OUTPUT_D,SpeedPercent, MoveTank, MoveDifferential, SpeedRPM, follow_for_ms
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor, GyroSensor
from ev3dev2.led import Leds
from ev3dev2.wheel import EV3Tire,Wheel
from ev3dev2.sound import Sound

import time
import math

def inch_to_cm(inch):
    return inch*2.54

def clamp(val,min,max):
    if val<min:
        return min
    if val>max:
        return max
    return val
#outputA is left motor
#outputB is right motor

#initialize wheel class
class MyWheel(Wheel):
    def __init__(self):
        Wheel.__init__(self, 56, 26) #wheel diameter is 68mm and 35mm width
        
left_wheel=OUTPUT_A
right_wheel=OUTPUT_D
med_motor=OUTPUT_B
wheel_distance=136
mdiff = MoveDifferential(left_wheel, right_wheel, MyWheel, wheel_distance)
isPicking=False

current_x=inch_to_cm(6)
current_y=inch_to_cm(-6)
current_angle=90

gyro=GyroSensor()
gyro.reset()
print("start calibrate")
gyro.calibrate()
print("done calibrate")

def updatePos(distance):
    global current_x,current_y,current_angle
    current_x+=distance*math.cos(math.radians(current_angle))
    current_y+=distance*math.sin(math.radians(current_angle))

#Move forwards a distance (cm)
#Stop if there is an object 12.7 cm (5 inches) infront
#Move forwards a distance (cm)
#Stop if there is an object 12.7 cm (5 inches) infront
def Forward(distance,speed=40,picking=False):
    gyro.reset()
    gyro.calibrate()
    init_angle=0
    mdiff.odometry_start(theta_degrees_start=90.0, x_pos_start=0.0, y_pos_start=0.0)
    mdiff.on_for_distance(SpeedRPM(-speed), distance*10, brake=True, block=False) #make sure block is False
    
    while mdiff.is_running:
        #print("distance in front: ",obstacle_detect())
        previously_traveled=abs(mdiff.y_pos_mm)/10.0
        print(previously_traveled,'  cm')
        # print(previously_traveled)
        # if previously_traveled>=distance:
        #     break
        if not picking and obstacle_detect()<=22.7: #and not isPicking
            #print("stop")
            mdiff.stop()
            quit()
            break
        #print(gyro.angle,'   ',init_angle)
        if (abs(gyro.angle-init_angle)>0):
            mdiff.stop()
            Rotate_CCW(-init_angle+gyro.angle,speed=20)
            gyro.reset()
            gyro.calibrate()
            mdiff.on_for_distance(SpeedRPM(-speed), (distance-previously_traveled)*10.0, brake=True, block=False)
            
        #print(mdiff.y_pos_mm)
    mdiff.stop()
    mdiff.odometry_stop()
    updatePos(distance)
    time.sleep(0.5)
    return

  
#Move backwards a distance (cm)  
def Reverse(distance,speed=30):
    mdiff.on_for_distance(SpeedRPM(speed),distance*10)
    updatePos(-distance)
    time.sleep(0.5)

def clamp_angle(angle_deg):
    angle_deg = angle_deg + 360.0
    mapped_angle = angle_deg % 360.0
    return mapped_angle

#Rotate counter clock wise an angle (degree)

#Rotate counter clock wise an angle (degree)
def Rotate_CCW(angle,speed=20):
    global current_x,current_y,current_angle
    time.sleep(2.0)
    gyro.reset()
    gyro.calibrate()
    angle=-angle
    #print('bruh,',angle)
    #mdiff.odometry_start(theta_degrees_start=0) 
    #mdiff.turn_degrees(SpeedRPM(20),(angle),brake=True)
    #mdiff.odometry_stop()
    a=gyro.angle
    motors = MoveTank(left_wheel,right_wheel)#angle/ang_vel+0.3) 
    passed=False
    error=0
    while not passed:
        while (abs(a+angle-gyro.angle)>0):
            #print(gyro.angle,'   ',a+angle)
            coef=1
            if gyro.angle<a+angle:
                coef=-1
            #if abs( (a+angle) - gyro.angle)<10:
            coef*=abs((a+angle) - gyro.angle)/50.0+0.5
            motors.on(SpeedRPM(speed*coef), SpeedRPM(-speed*coef))
        motors.stop(brake=True)
        time.sleep(2.0)
        #print(gyro.angle,'   ',a+angle)
        if abs(a+angle-gyro.angle)<=error:
            passed=True
    #print(gyro.angle,'   ',a+angle)
    #motors.stop(brake=True)
    current_angle+=angle
    current_angle=clamp_angle(current_angle)  
    
    time.sleep(0.5)
    #print('rotated angle:'+str(angle))
 
def obstacle_detect():
    us = UltrasonicSensor(INPUT_3)
    distance = us.distance_centimeters
    return distance

#1 is up
#-1 is down  
def moveForklift(direction):
    medium_motor = MediumMotor(med_motor)
    spd=0
    if direction==1:
        say("picking object")
        spd=100
        medium_motor.on_for_seconds(SpeedPercent(-spd*direction),15)
    elif direction==-1:
        say("dropping object")
        spd=20
        medium_motor.on_for_seconds(SpeedPercent(-spd*direction),15)
        #medium_motor.stop()


def say(sth):
    spkr=Sound()
    spkr.speak(sth)
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

def readBarcode(input=RIGHT_COLOR_SENSOR):
    barcode_read=[]
    color=readBnW(input)
    if (not color==not_bnw):
        for i in range(4):
            color=readBnW(input)
            barcode_read.append(color)
            if color==black:
                say('Black')
            elif color==white:
                say('White')
            else:
                say ("Not black or white")
            #mdiff.on_for_distance(SpeedRPM(-10), 1.27*10, brake=True, block=True)
            Forward(1.27,speed=20)
    #print(barcode_read)
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
            #print('found ', str(code))
            return code
    return -1

def read_code(input_sensor):
    while readBnW(input_sensor)==not_bnw:
        Forward(1,speed=10)
    code=readBarcode(LEFT_COLOR_SENSOR)
    sent="found code "+str(code)
    say(sent)
    return code

def sub_task3_task4(code_type):
    global current_angle, current_x
    moveForklift(1)
    Forward(inch_to_cm(11))
    code=read_code(LEFT_COLOR_SENSOR)
    if code==code_type:
        say("correct box")
        Forward(5.5,speed=15)
        mdiff.on_arc_right(SpeedRPM(-10), wheel_distance/2.0, 0.25*math.pi*wheel_distance, brake=True, block=True)
        current_angle-=90
        moveForklift(-1)
        Reverse(inch_to_cm(4.5),speed=10)
        moveForklift(1)
        print("correct box ")
        Rotate_CCW(90)
        Forward(102*2.54 - current_x)
        moveForklift(-1)
        
    else:
        say("wrong box")
        print("wrong box ")
        
"------------------------------------------------Khang--------------------------"
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

L_box = 36/6
distance_x = 0
distance_y = 0

def moving_to_shelf_subtask1_(shelf_choice,box_choice):
    for i in range (len(shelf)):
        if shelf_choice == shelf[i][1]: 
            if box_choice >= 1 and box_choice <7:
                
                distance_y = (shelf[i][0][1]-cp[1])*2.54
                distance_x = ((box_choice-1)*L_box+6)*2.54
                current_x = distance_x + cp[0]
                current_y = distance_y + cp[1]
                Forward(distance_y)
                Rotate_CCW(-87)
                Forward(distance_x)
                time.sleep(5)
                Forward(102*2.54-current_x-10)
                Rotate_CCW(-87)
                Forward(distance_y)
            else:
                
                distance_y = (shelf[i][0][1]-cp[1]+18)*2.54
                distance_x = ((box_choice-7)*L_box+6)*2.54
                current_x = distance_x + cp[0]
                current_y = distance_y + cp[1]
                Forward(distance_y)
                Rotate_CCW(-87)
                Forward(distance_x)
                time.sleep(5)
                Forward(102*2.54-current_x-10)
                Rotate_CCW(-87)
                Forward(distance_y)
    Rotate_CCW(180)
    global current_distance_x
    global current_distance_y
    current_distance_x = distance_x
    current_distance_y = distance_y

def moving_back_subtask2():
    Rotate_CCW(-180)
    Forward(12*2.54)
    Rotate_CCW(87)
    Forward((102-6)*2.54)
    Rotate_CCW(87)
    Forward(12*2.54)

def subtask3_subtask4():
    moveForklift(1)
    global color_read
    color_read =  []
    if box_choice > 1 and box_choice < 7:
        distance_x = box_choice*L_box
        Forward(distance_x)
    else:
        distance_x = (box_choice-12)
        Forward(distance_x)
    Forward(1.27)
    for i in range (4):
        color = readBnW(input=ColorSensor)
        print("The color is: " + str(color))
        Forward(1.27)
        color_read.append(color)

    mdiff.on_arc_right(SpeedRPM(-10),wheel_distance/2.0,100,brake=True,block = True)
    moveForklift(-1)
    moveForklift(1)

    new_distance_x = 36 - distance_x
    Forward(new_distance_x*2.54)
    moveForklift(-1)
