"""!
@file RoboMotorDriver.py
This motor driver utilizes the DRI0039 MotorDriver shield from DFRobot which
uses two TB6612FNG driver circuits to be able to cotnrol up to 4 motors. This
class is designed for use along with the Nucleo L476RG microcontroller with PWM
used to control speed with higher resolution and efficiency. 

@author Jonathan Cederquist
@author Tim Jain
@author Philip Pang

@date   3/2/22
"""
import pyb
import utime

class RoboMotorDriver:
    '''! 
    @brief This class allows instances of motors to be made and controlled individually
    '''
    duty_limit = 100
    def __init__ (self, dir_Pin, speed_Pin, timer_Num, channel_Num):
        '''! 
        @brief Instantiates motor driver by initializing GPIO pins and turning the motor off for safety. 
        @details A timer object is also made. This will be used to send PWM'd power to the motors
        
        @param dir_Pin       Pin object for setting motor direction: low() for fwd, high() for rev
        @param speed_Pin     Pin object for use with timer PWM channel to set motor speed
        @param timer_Num     An integer designating which timer to use for the pin objects specified
        @param channel_Num   An integer representing the channel used with the motor timer
        '''
        print ('Creating a robo motor driver')
        
        # Direction pin and speed pin
        self.dirPin = dir_Pin
        self.speedPin = speed_Pin
        
        # a timer object is created with pins configured to create PWM signals
        tim = pyb.Timer (timer_Num, freq=20000)
        self.ch = tim.channel(channel_Num, pyb.Timer.PWM, pin=self.speedPin)
        

    def set_duty_cycle (self, duty):
        '''!
        @brief This method sets the duty cycle to be sent to the motor to the given level. Positive values
        cause torque in one direction, negative values in the opposite direction.
        @param duty A signed integer representing desired duty cycle for the power sent to the motor 
        '''
        
        # CASE 1 & 2: positive duty cycle
        if duty > 0:
            self.dirPin.low()
            # CASE 1: duty cycle needs to be at MAX = 100%
            if duty > self.duty_limit:
                self.ch.pulse_width_percent(self.duty_limit)
            # CASE 2: duty cycle is below MAX = 100%
            else:
                self.ch.pulse_width_percent(duty)  
        
        # CASE 3 & 4: negative duty cycle
        elif duty < 0:
            self.dirPin.high()
            # CASE 3: duty cycle needs to be at MAX = 100%
            if duty < -self.duty_limit:
                self.ch.pulse_width_percent(self.duty_limit)
            # CASE 4: duty cycle is below MAX = 100%
            else:
                self.ch.pulse_width_percent(-duty)
        
        # CASE 5: duty cycle is zero
        else:
            self.ch.pulse_width_percent(0)

        
    def enable(self):
        '''!
        @brief This method should never be used
        '''
        pass
        
    def disable(self):
        '''!
        @brief This method should never be used
        '''
        pass
        
    
if __name__ == "__main__":
    '''!
    @brief Tests MotorDriver.py by creating two MotorDriver objects and sets them to different speeds
    '''
    # Instantiates three motor driver objects with appropriate pins and timer number
    pinB5 = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    pinB3 = pyb.Pin(pyb.Pin.board.PB3, pyb.Pin.OUT_PP)
    
    motor1 = RoboMotorDriver(pinB5, pinB3, 2, 2)
    
    # Motor 2
    pinA6 = pyb.Pin(pyb.Pin.board.PA6, pyb.Pin.OUT_PP)
    pinA7 = pyb.Pin(pyb.Pin.board.PA7, pyb.Pin.OUT_PP)
    
    motor2 = RoboMotorDriver(pinA6, pinA7, 3, 2)
    
    # Motor 3
    pinA9 = pyb.Pin(pyb.Pin.board.PA9, pyb.Pin.OUT_PP)
    pinB4 = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    
    motor3 = RoboMotorDriver(pinA9, pinB4, 3, 1)
    
    # Motor 4
    pinA8 = pyb.Pin(pyb.Pin.board.PA8, pyb.Pin.OUT_PP)
    pinB10 = pyb.Pin(pyb.Pin.board.PB10, pyb.Pin.OUT_PP)
    
    motor4 = RoboMotorDriver(pinA8, pinB10, 2, 3)
    
    # Enable motor 1 and 2
    motor1.set_duty_cycle(100)
    motor2.set_duty_cycle(100)
    motor3.set_duty_cycle(100)
    motor4.set_duty_cycle(100)
    # Stay at current state for 3 seconds
    utime.sleep(3)
    
    # Flip motor direction
    motor1.set_duty_cycle(25)
    motor2.set_duty_cycle(25)
    motor3.set_duty_cycle(25)
    motor4.set_duty_cycle(25)
    # Stay at current state for 3 seconds
    utime.sleep(3)
    
    # Test invalid duty cycle
    motor1.set_duty_cycle(-150)
    motor2.set_duty_cycle(-150)
    motor3.set_duty_cycle(-150)
    motor4.set_duty_cycle(-150)
    # Stay at current state for 3 seconds
    utime.sleep(3)
    
    # Stop motors
    motor1.set_duty_cycle(0)
    motor2.set_duty_cycle(0)
    motor3.set_duty_cycle(0)
    motor4.set_duty_cycle(0)
    
    
