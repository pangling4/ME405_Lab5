''' @file       ClosedLoop.py
    @brief      Implements closed loop proportional controller for position
    @details    Class of closed loop controller that can be used to control PITTMAN motors given in ME 405 lab
                with NUCLEO L476RG microcontroller
                
    @author     Jonathan Cederquist
    @author     Tim Jain
    @author     Philip Pang
    @date       Last Modified 2/2/22
'''

import pyb
import utime

class ClosedLoop:
    '''!
    @brief This class implements a closed loop proportional controller
    '''
    
    def __init__ (self, kp, ki, setpoint):
        '''! 
        @brief          Creates a ClosedLoop Controller object
        @details        Creates a ClosedLoop Controller object with the given
                        proportional control gain and reference value
        @param kp       Controller proportional gain in [% duty cycle/rad]
        @param ki       Controller integral gain [% duty cycle-s/rad]
        @param setpoint Reference value in rad for the system
        '''
        # Set controller proportional gain and setpoint
        self.kp = kp
        self.ki = ki
        self.setpoint = setpoint
        self.total_error = 0
        self.last_time = 0
        
    def update(self, measured):
        '''!
        @brief              Updates the control signal based on the current error
        @details            Implements PI control and returns the proportional
                            gain times the error (setpoint - actual position) added
                            to the integral gain times an approximation of the integral
                            of the error signal
        @param measured     The current position of the system [rad] to compare to the setpoint
        '''
        
        # Calculate error and proportional control signal
        error = self.setpoint - measured
        pro = self.kp*error
        
        if self.last_time==0:
            self.last_time = utime.ticks_ms()
            
        # Calculate integral control signal
        delta_t = utime.ticks_diff(utime.ticks_ms(), self.last_time)
        self.total_error += error*delta_t
        integ = self.ki*self.total_error
        
        self.last_time = utime.ticks_ms()
        
        # Return control signal
        return pro + integ
        
    def change_setpoint(self, setpoint):
        '''!
        @brief              Updates the setpoint of the controller
        @param setpoint     The new setpoint for the controller [rad]
        '''
        
        self.setpoint = setpoint
        
    def change_kp(self, kp):
        '''!
        @brief       Updates the proportional gain value of the controller
        @param kp    The new proportional gain for the controller [% duty cycle/rad]
        '''
        
        self.kp = kp
        
    def change_ki(self, ki):
        '''!
        @brief       Updates the integral gain value of the controller
        @param ki    The new integral gain for the controller [% duty cycle-s/rad]
        '''
        
        self.ki = ki