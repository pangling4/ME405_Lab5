''' @file
    @brief
    @details

    @author         Philip Pang
    @author         Matthew Wimberley
    @date           October 26, 2021
'''

import pyb
import utime
import TouchDriver

class TaskTouch:
    '''@brief       instantiates self object of Touch Panel tasks'''

    prev_state = (0,0,0)

    def __init__(self, ready, touchpad_x, touchpad_y):

        '''@brief
           @param
        '''
        self.ready = ready
        self.touchpad_x = touchpad_x
        self.touchpad_y = touchpad_y
        self.TouchPanel = TouchDriver.TouchDriver(pyb.Pin.board.PC3, pyb.Pin.board.PC0, pyb.Pin.board.PC2, pyb.Pin.board.PB0)
        self.TouchPanel.calibrate()

    def run(self):
        # @brief
        
        while True:
            contact = self.TouchPanel.scan_all()
            if contact[2]:
                self.touchpad_x.put(contact[0]/25.4 + 8.875)
                self.touchpad_y.put(contact[1]/25.4 + 5.124)
            yield(0)
