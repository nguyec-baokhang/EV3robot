#!/usr/bin/env python3
from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.led import Leds
import time
import math
#outputA is left motor
#outputB is right motor

#Move forwards a distance (cm)
def Forward(distance):
    vel=146.0/5.0   #cm per second
    med_mot_sped=-30.0
    large_mot_sped=med_mot_sped*1.5
    #motors = MoveTank(OUTPUT_A,OUTPUT_B)
    #motors.on_for_rotations(SpeedPercent(-40), SpeedPercent(-40), distance/vel)
    medium_motor = MediumMotor(OUTPUT_A)
    large_motor = LargeMotor(OUTPUT_B)
    
    medium_motor.on(med_mot_sped)
    large_motor.on_for_seconds(large_mot_sped,distance/vel)

    # Stop motors after execution
    medium_motor.stop(stop_action="brake")
    large_motor.stop(stop_action="brake")
  
#Move backwards a distance (cm)  
def Reverse(distance):
    vel=146.0/5.0  #cm per second
    med_mot_sped=30.0
    large_mot_sped=med_mot_sped*1.5
    #motors = MoveTank(OUTPUT_A,OUTPUT_B)
    #motors.on_for_rotations(SpeedPercent(40), SpeedPercent(40), distance/vel)
    medium_motor = MediumMotor(OUTPUT_A)
    large_motor = LargeMotor(OUTPUT_B)
    
    medium_motor.on(med_mot_sped)
    large_motor.on_for_seconds(large_mot_sped,distance/vel)

    # Stop motors after execution
    medium_motor.stop(stop_action="brake")
    large_motor.stop(stop_action="brake")
#Rotate counter clock wise an angle (degree)
def Rotate_CCW(angle):
    #ang_vel=162.0  #degs per second
    med_mot_sped=10.0
    large_mot_sped=-med_mot_sped*1.5
    #motors = MoveTank(OUTPUT_A,OUTPUT_B)
    #motors.on_for_rotations(SpeedPercent(40), SpeedPercent(40), distance/vel)
    medium_motor = MediumMotor(OUTPUT_A)
    large_motor = LargeMotor(OUTPUT_B)
    
    gyro=GyroSensor()
    gyro.reset()
    print("start calibrate")
    gyro.calibrate()
    print("done calibrate")
    print(gyro.angle)
    a=gyro.angle

    while (abs(gyro.angle-a)<angle-10):
        print(abs(gyro.angle-a))
        #motors = MoveTank(OUTPUT_A,OUTPUT_B)
        #motors.on_for_rotations(SpeedPercent(50), SpeedPercent(-50), 0.1)#angle/ang_vel+0.3)  
        medium_motor.on(med_mot_sped)
        large_motor.on_for_seconds(large_mot_sped,0.01)

    # Stop motors after execution
    medium_motor.stop(stop_action="brake")
    large_motor.stop(stop_action="brake")  

