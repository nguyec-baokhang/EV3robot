#!/usr/bin/env python3
from ev3dev2.motor import *

steer_pair = MoveSteering(OUTPUT_A,OUTPUT_B)


m_left = Motor(OUTPUT_A)
m_right = Motor(OUTPUT_B)
tank_pair = MoveTank(OUTPUT_A, OUTPUT_B)
i = 0
n = int(input("Give the number of laps: "))

while i <= n: 
    tank_pair.on_for_seconds(left_speed=-50, right_speed=-50,seconds = 5)
    steer_pair.on_for_degrees(steering=100,speed=20,degrees=180)
    tank_pair.on_for_seconds(left_speed=-50, right_speed=-50,seconds = 5)
    i += 1