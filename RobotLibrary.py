#!/usr/bin/env python3
from ev3dev2.motor import MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_D,SpeedPercent, MoveTank, MoveDifferential, SpeedRPM
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.led import Leds
from ev3dev2.wheel import EV3Tire,Wheel
#outputA is left motor
#outputB is right motor


class MyWheel(Wheel):
    def __init__(self):
        Wheel.__init__(self, 70, 35) #wheel diameter is 70mm and 35 width
        
left_wheel=OUTPUT_A
right_wheel=OUTPUT_D
med_motor=OUTPUT_B
wheel_distance=130.5
mdiff = MoveDifferential(left_wheel, right_wheel, MyWheel, wheel_distance)

#Move forwards a distance (cm)
def Forward(distance):
    #vel=9.91   #cm per second
    #motors = MoveTank(left_wheel,right_wheel)
    #motors.on_for_seconds(SpeedPercent(-15), SpeedPercent(-15), distance/vel,brake=True)
    mdiff.on_for_distance(SpeedRPM(-30),distance*10)
  
#Move backwards a distance (cm)  
def Reverse(distance):
    #vel=9.91  #cm per second
    #motors = MoveTank(left_wheel,right_wheel)
    #motors.on_for_seconds(SpeedPercent(15), SpeedPercent(15), distance/vel,brake=True)
    mdiff.on_for_distance(SpeedRPM(30),distance*10)

#Rotate counter clock wise an angle (degree)
def Rotate_CCW(angle):
    #ang_vel=162.0  #degs per second
    med_mot_sped=10.0
    large_mot_sped=-med_mot_sped*1.5
    #motors = MoveTank(OUTPUT_A,OUTPUT_B)
    #motors.on_for_rotations(SpeedPercent(40), SpeedPercent(40), distance/vel)
    
    #gyro=GyroSensor()
    #gyro.reset()
    #print("start calibrate")
    #gyro.calibrate()
    #print("done calibrate")
    #print(gyro.angle)
    #a=gyro.angle
    #motors = MoveTank(left_wheel,right_wheel)
    #while (abs(gyro.angle-a)<angle-9):
    #    print(abs(gyro.angle-a))
    #    motors.on(SpeedPercent(15), SpeedPercent(-15))#angle/ang_vel+0.3)  
    #motors.stop()
    
    mdiff.odometry_start(theta_degrees_start=0.0)
    mdiff.turn_degrees(SpeedRPM(30),-(angle))
    mdiff.odometry_stop()
    
def moveMed(sth):
    medium_motor = MediumMotor(med_motor)
    medium_motor.on_for_seconds(-30,5)


#move

#Forward(20)
#Rotate_CCW(180)
#moveMed(3)