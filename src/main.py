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
        
# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":    
    
    # Create queues for x and y touchpad positions
    touchpad_x = task_share.Queue('f', 100, thread_protect = False, name = "touchpad_x")
    touchpad_y = task_share.Queue('f', 100, thread_protect = False, name = "touchpad_y")
    
    # Create queues for joint positions
    theta_1 = task_share.Queue('f', 100, thread_protect = False, name = "theta_1", overwrite = True)
    theta_2 = task_share.Queue('f', 100, thread_protect = False, name = "theta_2", overwrite = True)
    theta_3 = task_share.Queue('f', 100, thread_protect = False, name = "theta_3", overwrite = True)
    
    # Create RoboBrain with robot geometry
    myRoboBrain = RoboBrain.RoboBrain([0,0], [17.75, 0], [8.875, 15.375], 7.25, 7.25, [-1.985, -1.089], \
                                    [1.829, -1.089], [-0.244, 2.144])
    # Create task objects
    Joint1 = JointTask.JointTask(1, 1, 0.7, 0.05, 0, theta_1)
    Joint2 = JointTask.JointTask(2, 2, 0.7, 0.05, 0, theta_2)
    Joint3 = JointTask.JointTask(3, 3, 0.7, 0.05, 0, theta_3)
    Brain = RoboTask.RoboTask(myRoboBrain, touchpad_x, touchpad_y, theta_1, theta_2, theta_3)   
    
    # Putting task objects in cotask run list
    task1_J1 = cotask.Task(Joint1.run, name = 'Task1_J1', priority = 2,
                             period = 10, profile = True, trace = False)
    
    task2_J2 = cotask.Task(Joint2.run, name = 'Task1_J2', priority = 2, 
                              period = 10, profile = True, trace = False)
    
    task3_J3 = cotask.Task(Joint3.run, name = 'Task1_J3', priority = 2, 
                              period = 10, profile = True, trace = False)
            
    task4_B = cotask.Task(Brain.run, name = 'Task4_B', priority = 3,
                              period = 10, profile = True, trace = False)
    
    cotask.task_list.append(task1_J1)
    cotask.task_list.append(task2_J2)
    cotask.task_list.append(task3_J3)
    cotask.task_list.append(task4_B)

    Contperiod = int(input("Set Controller Period: "))
    Contperiod2 = int(input("Set Second Controller Period: "))
    
    # Set period of controller based on user input
    task3_Cont.set_period(Contperiod)
    task6_Cont2.set_period(Contperiod2)
    
    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()
    
    while True:
        try:
            cotask.task_list.pri_sched ()
                
        except KeyboardInterrupt:
            print("End Program")
            share_duty_1.put(0)
            share_duty_2.put(0)
            task1_Mot.schedule()
            task4_Mot2.schedule()
            break
        
    