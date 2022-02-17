''' @file
    @brief
    @details

    @author         Philip Pang
    @author         Matthew Wimberley
    @date           October 26, 2021
'''

import utime

class TouchTasks:
    '''@brief       instantiates self object of Touch Panel tasks'''

    prev_state = (0,0,0)

    def __init__(self, freq_io, Touch_Panel, balancing, collect, touch_state):

        '''@brief
           @param
           '''

        self.freq_io = freq_io
        self.period = 1 / freq_io * 1000000  # in us (microseconds)
        self.next_time = 0

        self.TouchPanel = Touch_Panel

        self.balancing = balancing
        self.collect = collect
        self.touch_state = touch_state

    def run(self):
        # @brief
        if (utime.ticks_us() >= self.next_time):
            '''@brief       
               @details     
               @param       must call object of itself
               '''
            self.next_time = utime.ticks_us() + self.period

            ball = self.TouchPanel.scan_all()
            velocity = (0,0)

            if not ball[2]:
                ball = (0,0, False)         # if ball is not in contact, read ball as being at equilibrium
                self.prev_state = (0,0,0)   # if ball is not in contact, zero previous prev_state so alg will know exactly when it comes into contact
                # velocity = (0, 0)         # if ball is not in contact, zero velocity
            else:
                if self.prev_state == (0,0,0):      # when ball comes INTO contact for the first time
                    self.prev_state = ball
                    # velocity = (0, 0)             # if ball is not in contact, zero velocity
                else:                               # when ball is IN contact and HAS BEEN
                    velocity = (((ball[0]-self.prev_state[0])*self.freq_io ), ((ball[1]-self.prev_state[1])*self.freq_io))
                    self.prev_state = ball

            self.touch_state.write((ball[0], ball[1], velocity[0], velocity[1], ball[2])) # (x_scan, y_scan, x_vel, y_vel, z_scan)

