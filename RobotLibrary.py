#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds

#outputA is left motor
#outputB is right motor

#Move forwards a distance (cm)
def Forward(distance):
    vel=90.0/4   #inches per second
    motors = MoveTank(OUTPUT_A,OUTPUT_B)
    motors.on_for_rotations(SpeedPercent(-75), SpeedPercent(-75), distance/vel)
  
#Move backwards a distance (cm)  
def Reverse(distance):
    vel=90.0/4   #inches per second
    motors = MoveTank(OUTPUT_A,OUTPUT_B)
    motors.on_for_rotations(SpeedPercent(75), SpeedPercent(75), distance/vel)
    
#Rotate counter clock wise an angle (degree)
def Rotate_CCW(angle):
    ang_vel=309.0/2.0  #degs per second
    motors = MoveTank(OUTPUT_A,OUTPUT_B)
    motors.on_for_rotations(SpeedPercent(50), SpeedPercent(-50), angle/ang_vel)    
    