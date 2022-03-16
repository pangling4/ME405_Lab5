'''!
@file     TaskTouch.py
@brief    This file interfaces with the touchpanel that the 3RRR robot reads coordinate data from.
@details  This task determines if the touchpanel is being touched and if it is, it adds coordinates
          to a queue for the RoboTask to process using the RoboBrain to determine appropriate motor angles. 
    
@author Jonathan Cederquist
@author Tim Jain
@author Philip Pang
@date   Last Modified 3/15/22
'''

import pyb
import utime
import TouchDriver

class TaskTouch:
    '''!
        @brief       instantiates self object of Touch Panel tasks
    '''

    def __init__(self, ready, touchpad_x, touchpad_y):
        '''!
            @brief Assigns shared communication variables to be accessible locally and instantiates
                   touch panel driver for touch panel interfacing.
            @param ready       The task_share.Share corresponding to whether or not the touchpanel
                               should be recording data because the robot is READY to draw
            @param touchpad_x  The task_share.Queue corresponding to x_coordinate in inches on the
                               coordinate system of the drawing area of the 3RRR robot
            @param touchpad_y  The task_share.Queue corresponding to y_coordinate in inches on the
                               coordinate system of the drawing area of the 3RRR robot
        '''
        self.ready = ready
        self.touchpad_x = touchpad_x
        self.touchpad_y = touchpad_y
        self.TouchPanel = TouchDriver.TouchDriver(pyb.Pin.board.PC3, pyb.Pin.board.PC0, pyb.Pin.board.PC2, pyb.Pin.board.PB0)
        self.TouchPanel.calibrate()

    def run(self):
        # @brief
        
        while True:
            # scans the touch panel contact is tuple: (x_coordinate (mm), y_coordinate (mm), touched or not? (binary))
            contact = self.TouchPanel.scan_all()
            # if touch panel is being touched, add x and y coordinates to their respective queues
            if contact[2]:
                self.touchpad_x.put(contact[0]/15 + 8.875)
                self.touchpad_y.put(contact[1]/15 + 5.124)
            yield(0)
