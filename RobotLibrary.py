#!/usr/bin/env python3
from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.led import Leds
#outputA is left motor
#outputB is right motor

#Move forwards a distance (cm)
def Forward(distance):
    vel=9.91   #cm per second
    motors = MoveTank(OUTPUT_A,OUTPUT_B)
    motors.on_for_seconds(SpeedPercent(-15), SpeedPercent(-15), distance/vel,brake=True)
  
#Move backwards a distance (cm)  
def Reverse(distance):
    vel=9.91  #cm per second
    motors = MoveTank(OUTPUT_A,OUTPUT_B)
    motors.on_for_seconds(SpeedPercent(15), SpeedPercent(15), distance/vel,brake=True)

#Rotate counter clock wise an angle (degree)
def Rotate_CCW(angle):
    #ang_vel=162.0  #degs per second
    med_mot_sped=10.0
    large_mot_sped=-med_mot_sped*1.5
    #motors = MoveTank(OUTPUT_A,OUTPUT_B)
    #motors.on_for_rotations(SpeedPercent(40), SpeedPercent(40), distance/vel)
    
    gyro=GyroSensor()
    gyro.reset()
    print("start calibrate")
    gyro.calibrate()
    print("done calibrate")
    print(gyro.angle)
    a=gyro.angle
    motors = MoveTank(OUTPUT_A,OUTPUT_B)
    while (abs(gyro.angle-a)<angle-9):
        print(abs(gyro.angle-a))
        motors.on(SpeedPercent(15), SpeedPercent(-15))#angle/ang_vel+0.3)  
    motors.stop()