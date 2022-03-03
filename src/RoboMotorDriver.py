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

    def __init__ (self, dir_Pin, speed_Pin, timer_Num):
        '''! 
        @brief Instantiates motor driver by initializing GPIO pins and turning the motor off for safety. 
        @details A timer object is also made. This will be used to send PWM'd power to the motors
        
        @param dir_Pin   Pin object for setting motor direction: low() for fwd, high() for rev
        @param speed_Pin Pin object for use with timer PWM channel to set motor speed
        @param timer     An integer designating which timer to use for the pin objects specified
        '''
        print ('Creating a robo motor driver')
        
        # Direction pin and speed pin
        self.dirPin = dir_Pin
        self.speedPin = speed_Pin
        
        # a timer object is created with pins configured to create PWM signals
        tim = pyb.Timer (timer_Num, freq=20000)
        self.ch2 = tim.channel (2, pyb.Timer.PWM, pin=self.speedPin)
        

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
            if duty > 100:
                self.ch2.pulse_width_percent(100)
            # CASE 2: duty cycle is below MAX = 100%
            else:
                self.ch2.pulse_width_percent(duty)  
        
        # CASE 3 & 4: negative duty cycle
        elif duty < 0:
            self.dirPin.high()
            # CASE 3: duty cycle needs to be at MAX = 100%
            if duty < -100:
                self.ch2.pulse_width_percent(100)
            # CASE 4: duty cycle is below MAX = 100%
            else:
                self.ch2.pulse_width_percent(-duty)
        
        # CASE 5: duty cycle is zero
        else:
            self.ch2.pulse_width_percent(0)

        
    def enable(self):
        '''!
        @brief This method enables the motor by setting the sleep pin to high
        '''
        pass
        
    def disable(self):
        '''!
        @brief This method disables the motor by setting the sleep pin to low
        '''
        self.ch2.pulse_width_percent(0)
        
if __name__ == "__main__":
    '''!
    @brief Tests MotorDriver.py by creating two MotorDriver objects and sets them to different speeds
    '''
    # Instantiates two motor driver objects with appropriate pins and timer number
    pinB5 = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    pinB3 = pyb.Pin(pyb.Pin.board.PB3, pyb.Pin.OUT_PP)
    
    motor1 = RoboMotorDriver(pinB5, pinB3, 2)
    
    # Enable motor 1 and 2
    motor1.set_duty_cycle(50)
    # Stay at current state for 3 seconds
    utime.sleep(3)
    
    # Flip motor direction
    motor1.set_duty_cycle(-50)
    # Stay at current state for 3 seconds
    utime.sleep(3)
    
    # Test invalid duty cycle
    motor1.set_duty_cycle(-150)
    # Stay at current state for 3 seconds
    utime.sleep(3)
    
    # Stop motors
    motor1.set_duty_cycle(10)
    motor1.disable()

    
