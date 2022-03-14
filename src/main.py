"""!
@file main.py
    This file contains tasks to simultaneously perform closed loop control
    on two Pittman motors in ME 405 Lab
    
@author Jonathan Cederquist
@author Tim Jain
@author Philip Pang
@date   Last Modified 2/3/22
"""

import gc
# import pyb
import math
import utime
import cotask
import task_share

import JointTask
import TaskTouch

import RoboBrain
import RoboTask
        

if __name__ == "__main__":    
    
    # Create queues for x and y touchpad positions
    touchpad_x = task_share.Queue('f', 100, thread_protect = False, name = "touchpad_x")
    touchpad_y = task_share.Queue('f', 100, thread_protect = False, name = "touchpad_y")
    
    # Create share to synchronize start, stop of drawing
    ready = task_share.Share('i', thread_protect = False, name = "drawing")
    ready.put(1)

    
    # Create queues for joint positions
    theta_1 = task_share.Queue('f', 100, thread_protect = False, name = "theta_1", overwrite = True)
    theta_2 = task_share.Queue('f', 100, thread_protect = False, name = "theta_2", overwrite = True)
    theta_3 = task_share.Queue('f', 100, thread_protect = False, name = "theta_3", overwrite = True)
        
    # Create RoboBrain with robot geometry
    myRoboBrain = RoboBrain.RoboBrain([0,0], [17.75, 0], [8.875, 15.375], 7.25, 7.25, [-1.985, -1.089],
                                    [1.829, -1.089], [-0.244, 2.144])
    # Create task objects
    Brain = RoboTask.RoboTask(ready, myRoboBrain, touchpad_x, touchpad_y, theta_1, theta_2, theta_3)   
    Touch = TaskTouch.TaskTouch(ready, touchpad_x, touchpad_y)
    Joint1 = JointTask.JointTask(ready, 1, 1, 0.9, 0.05, 0, theta_1)
    Joint2 = JointTask.JointTask(ready, 2, 2, 0.9, 0.05, 0, theta_2)
    Joint3 = JointTask.JointTask(ready, 3, 3, 0.9, 0.05, 0, theta_3)
    Brain = RoboTask.RoboTask(ready, myRoboBrain, touchpad_x, touchpad_y, theta_1, theta_2, theta_3)   
    
    # Putting task objects in cotask run list
    task1_J1 = cotask.Task(Joint1.run, name = 'Task1_J1', priority = 2,
                             period = 50, profile = True, trace = False)
    
    task2_J2 = cotask.Task(Joint2.run, name = 'Task1_J2', priority = 2, 
                              period = 50, profile = True, trace = False)
    
    task3_J3 = cotask.Task(Joint3.run, name = 'Task1_J3', priority = 2, 
                              period = 50, profile = True, trace = False)
            
    task4_B = cotask.Task(Brain.run, name = 'Task4_B', priority = 3,
                              period = 50, profile = True, trace = False)
    
    task5 = cotask.Task(Touch.run, name = 'Task5', priority = 4,
                              period = 50, profile = True, trace = False)
    
    cotask.task_list.append(task1_J1)
    cotask.task_list.append(task2_J2)
    cotask.task_list.append(task3_J3)
    cotask.task_list.append(task4_B)
    cotask.task_list.append(task5)
    
    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    input("Press enter to start")
    
    while True:
        try:
            cotask.task_list.pri_sched()
                
        except KeyboardInterrupt:
            print("End Program")
            ready.put(0)
            utime.sleep_ms(50)
            task1_J1.schedule()
            task2_J2.schedule()
            task3_J3.schedule()
            task4_B.schedule()

            break
        
    