''' @file       RoboEncoderDriver.py
    @brief      Used to read from encoders attached to motors (No. GB37Y3530-12V-83R)
    @details    Utilizes alternate functions from timer channels on pyb board to 
                read from attached encoders
    @author     Jonathan Cederquist
    @author     Tim Jain
    @author     Philip Pang
    @date       Last Modified 3/3/22
'''

import pyb
import utime
import RoboMotorDriver

class RoboEncoderDriver:
    '''! 
    This class implements an encoder driver for an ME 405 Robot. 
    '''
    
    def __init__ (self, in1pin, in2pin, timer):
        '''! 
        @brief          Creates an encoder driver object
        @details        Creates an encoder driver by initializing timers and channels with 
                        given pins and timer number
        @param in1pin   A pyb.Pin object corresponding to the encoder channel A 
        @param in2pin   A pyb.Pin object corresponding to the encoder channel B
        @param timer    The timer number corresponding to the encoder pins
        '''
        
        # Create timer and timer channels in encoder mode
        self.timer = pyb.Timer(timer, prescaler = 0, period = 65535)
        self.ch1 = self.timer.channel(1, pyb.Timer.ENC_A, pin = in1pin)
        self.ch2 = self.timer.channel(2, pyb.Timer.ENC_B, pin = in2pin)
        
        # Stores current encoder position in radians
        self.current_position = 0
        self.delta = 0
        

    def update(self):
        '''!
        @brief      Updates the position of the encoder 
        @details    Updates the position of the encoder using saved last value
                    Checks for a 'valid' delta and adjusts if needed, then adds
                    delta to previous position 
        '''

        prev_position = self.current_position % 65535
        self.delta = self.timer.counter() - prev_position
        
        # Validate and adjust delta
        if self.delta < -65535/2:
            self.delta += 65535
        elif self.delta > 65535/2:
            self.delta -= 65535
        
        # Update position
        self.current_position += self.delta
        return self.current_position
    
    def read (self):
        '''!
        @brief      Returns current position of encoder
        @details    Converts the current encoder position reading (in ticks)
                    to degrees using the encoder CPR and gear ratio
        '''
        gearRatio = 131
        CPR = 16
        
        return self.current_position * 180 / (gearRatio*CPR)
    

    def zero(self):
        '''!
        @brief      Zeros the encoder position
        '''
        
        self.current_position = 0
        self.delta = 0
        self.timer.counter(0)
        
        
if __name__ == "__main__":
    
    encoder1 = RoboEncoderDriver(pyb.Pin(pyb.Pin.board.PB6), pyb.Pin(pyb.Pin.board.PB7), 4)
    encoder2 = RoboEncoderDriver(pyb.Pin(pyb.Pin.board.PC6), pyb.Pin(pyb.Pin.board.PC7), 8)
    encoder3 = RoboEncoderDriver(pyb.Pin(pyb.Pin.board.PA0), pyb.Pin(pyb.Pin.board.PA1), 5)
    
    
    # Instantiates three motor driver objects with appropriate pins and timer number
    pinB5 = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    pinB3 = pyb.Pin(pyb.Pin.board.PB3, pyb.Pin.OUT_PP)
    
    motor1 = RoboMotorDriver.RoboMotorDriver(pinB5, pinB3, 2, 2)
    
    # Motor 2
    pinA6 = pyb.Pin(pyb.Pin.board.PA6, pyb.Pin.OUT_PP)
    pinA7 = pyb.Pin(pyb.Pin.board.PA7, pyb.Pin.OUT_PP)
    
    motor2 = RoboMotorDriver.RoboMotorDriver(pinA6, pinA7, 3, 2)
    
    # Motor 3
    pinA9 = pyb.Pin(pyb.Pin.board.PA9, pyb.Pin.OUT_PP)
    pinB4 = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    
    motor3 = RoboMotorDriver.RoboMotorDriver(pinA9, pinB4, 3, 1)
    
    # Start motor 1, 2, 3
    motor1.set_duty_cycle(25)
    motor2.set_duty_cycle(25)
    motor3.set_duty_cycle(25)
    
    time = utime.ticks_ms()
    
    #while utime.ticks_ms() < (time + 10000):
    while True:
        encoder1.update()
        encoder2.update()
        encoder3.update()
        
        if (utime.ticks_ms() > (time + 50)):
            print("\ntimer counter1:", encoder1.timer.counter())
            print("\nencoder driver1", encoder1.read())
            
            print("\ntimer counter2:", encoder2.timer.counter())
            print("\nencoder driver2", encoder2.read())
            
            print("\ntimer counter3:", encoder3.timer.counter())
            print("\nencoder driver3", encoder3.read())
            
            if encoder1.read() > 360:
                break
            time += 50
    
    motor1.set_duty_cycle(0)
    motor2.set_duty_cycle(0)
    motor3.set_duty_cycle(0)
