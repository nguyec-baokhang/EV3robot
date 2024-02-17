#!/usr/bin/env python3
import RobotLibrary as rl
import time
n=5
distance=100  #cm
for i in range(0,n):
    rl.Forward(distance)
    time.sleep(0.5)
    rl.Rotate_CCW(180)
    time.sleep(0.5)
    rl.Forward(distance)
    time.sleep(0.5)
    rl.Rotate_CCW(180)
    time.sleep(0.5)
