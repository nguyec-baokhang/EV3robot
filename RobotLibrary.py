#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.led import Leds
import time
#outputA is left motor
#outputB is right motor
gyro=""
def Setup():
    gyro=GyroSensor()
    gyro.reset()
    print("start calibrate")
    gyro.calibrate()
    print("done calibrate")
#Move forwards a distance (cm)
def Forward(distance):
    vel=45.0/2   #cm per second
    motors = MoveTank(OUTPUT_A,OUTPUT_B)
    motors.on_for_rotations(SpeedPercent(-40), SpeedPercent(-40), distance/vel)
  
#Move backwards a distance (cm)  
def Reverse(distance):
    vel=45.0/2   #cm per second
    motors = MoveTank(OUTPUT_A,OUTPUT_B)
    motors.on_for_rotations(SpeedPercent(40), SpeedPercent(40), distance/vel)
    
#Rotate counter clock wise an angle (degree)
def Rotate_CCW(angle):
    #ang_vel=162.0  #degs per second

    a=gyro.angle()
    while ((gyro.angle()-a)<angle):
        motors = MoveTank(OUTPUT_A,OUTPUT_B)
        motors.on_for_rotations(SpeedPercent(50), SpeedPercent(-50), 0.1)#angle/ang_vel+0.3)    

def get_Angle():
    return gyro.angle