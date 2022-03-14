"""!
@file RoboSolenoidDriver.py
This solenoid driver utilizes the DRI0039 MotorDriver shield from DFRobot which
uses two TB6612FNG driver circuits to be able to control up to 4 motors. This
class is designed for use along with the Nucleo L476RG microcontroller to control
the motion of a solenoid by setting the pin high or low. 

@author Jonathan Cederquist
@author Tim Jain
@author Philip Pang

@date   3/9/22
"""
import pyb
import utime

class RoboSolenoidDriver:
    '''! 
    @brief This class allows a solenoid to be controlled using the motor driver shield
    '''

    def __init__ (self, dir_Pin, speed_Pin, timer_Num, channel_Num):
        '''! 
        @brief Instantiates solenoid driver by initializing GPIO pins. 
        @details A timer object is also made. This will be used to send PWM'd power to the solenoid
        
        @param dir_Pin       Pin object for setting motor direction: low() for fwd, high() for rev
        @param speed_Pin     Pin object for use with timer PWM channel to set motor speed
        @param timer_Num     An integer designating which timer to use for the pin objects specified
        @param channel_Num   An integer representing the channel used with the motor timer
        '''
        print ('Creating a robo solenoid driver')
        
        # Direction pin and speed pin
        self.dirPin = dir_Pin
        self.speedPin = speed_Pin
        
        # a timer object is created with pins configured to create PWM signals
        tim = pyb.Timer (timer_Num, freq=20000)
        self.ch = tim.channel(channel_Num, pyb.Timer.PWM, pin=self.speedPin)
        
        # Initialize direction pin to reverse
        self.dirPin.high()

    def pull_up(self):
        '''!
        @brief This method pulls up the solenoid plunger
        '''
        # Set duty cycle to max
        self.ch.pulse_width_percent(95)
        
    def push_down(self):
        '''!
        @brief This method releases the solenoid plunger
        '''
        
        # Set duty cycle to 0
        self.ch.pulse_width_percent(0)
        
        
if __name__ == "__main__":
    '''!
    @brief Tests RoboSolenoidDriver.py by creating a solenoid and pulling and pushing the plunger
    '''
    # Instantiates solenoid driver object with appropriate pins and timer number
    
    # Solenoid (Port 4)
    pinA8 = pyb.Pin(pyb.Pin.board.PA8, pyb.Pin.OUT_PP)
    pinB10 = pyb.Pin(pyb.Pin.board.PB10, pyb.Pin.OUT_PP)
    
    solenoid = RoboSolenoidDriver(pinA8, pinB10, 2, 3)
    
    # Pull solenoid up
    solenoid.pull_up()
    print("Pull up solenoid")
    utime.sleep(3)
    
    # Push down
    solenoid.push_down()
    print("Push down solenoid")
    utime.sleep(3)
    
    # Pull up
    solenoid.pull_up()
    print("Pull up solenoid")
    utime.sleep(5)
    
    solenoid.push_down()
    print("Push down solenoid")
    

