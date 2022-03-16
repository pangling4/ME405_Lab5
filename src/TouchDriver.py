'''!
@file            Touch_Panel.py
@brief           Controls the touch panel of the 3RRR robot which is designed to imitate and
                draw whenever and wherever the user touches the panel
@details         If there is pressure on the screen (i.e. touch), current is allowed to pass
                through the resistors leading to a voltage drop measured across the board's 
                pins.

@author          Philip Pang
@author          Matthew Wimberley
@date            November 16, 2021      

'''   

from pyb import Pin, ADC
import utime
from ulab import numpy as np
import os

class TouchDriver:
    
    '''!
        @brief       sets up pin read out values for xyz scanner
        @details     takes in each pin and board dimensions to set up origin
    '''

    k_xx = 170/4095
    k_xy = 0
    k_yx = 0
    k_yy = 100/4095
    x_offset = -100
    y_offset = -58

    def __init__(self, Pin_xp, Pin_xm, Pin_yp, Pin_ym):
        
        '''!
            @brief       instantiates touch panel pins
            @details     adjusts scaling using 2^12 total count
            @param       the four push pins
            @param       touch panel dimensions
            @param       origin offset to calibrate the panel's center
           '''
           
        self.Pin_xp = Pin_xp
        self.Pin_xm = Pin_xm
        self.Pin_yp = Pin_yp
        self.Pin_ym = Pin_ym

    def xy_scan(self):
        xp = Pin(self.Pin_xp, Pin.OUT_PP)
        xp.value(1)
        xm = Pin(self.Pin_xm, Pin.OUT_PP)
        xm.value(0)
        yp = Pin(self.Pin_yp, Pin.IN)
        ym = ADC(self.Pin_ym)
        ADCx = ym.read()
        yp = Pin(self.Pin_yp, Pin.OUT_PP)
        yp.value(1)
        ym = Pin(self.Pin_ym, Pin.OUT_PP)
        ym.value(0)
        xp = Pin(self.Pin_xp, Pin.IN)
        xm = ADC(self.Pin_xm)
        ADCy = xm.read()
        return(ADCx, ADCy)

    def x_scan(self):
        
        '''@brief       instantiates x axis pins
           @details     2 outputs correspond to the pin resistor set up
                        1 output is set up for the voltage read out and the 
                        forth pin is the input delivering the floating contact.
           @param       self
           '''
           
        ADC = self.xy_scan()
        return ADC[0] * self.k_xx + ADC[1] * self.k_xy + self.x_offset
        
    def y_scan(self):
        
        '''@brief       instantiates y axis pins
           @details     2 outputs correspond to the pin resistor set up
                        1 output is set up for the voltage read out and the 
                        forth pin is the input delivering the floating contact.
           @param       self
           '''
           
        ADC = self.xy_scan()
        return ADC[0] * self.k_yx + ADC[1] * self.k_yy + self.y_offset
        
    def z_scan(self):
        
        '''@brief       instantiates z axis pins
           @details     2 outputs correspond to the pin resistor set up
                        1 output is set up for the voltage read out and the 
                        forth pin is the input delivering the floating contact.
                        This scan returns true if the ball is making contact with
                        the touch panel.
           @param       self
        '''
        
        yp = Pin(self.Pin_yp, Pin.OUT_PP)
        yp.value(1)
        xm = Pin(self.Pin_xm, Pin.OUT_PP)
        xm.value(0)
        xp = Pin(self.Pin_xp, Pin.IN)
        ym = ADC(self.Pin_ym)
        return ym.read() < 4000
    
    def scan_all(self):
        
        '''@brief       scans all three coordinates simultaneously
        '''
        ADC = self.xy_scan()
        return ( ADC[0] * self.k_xx + ADC[1] * self.k_xy + self.x_offset,
                 ADC[0] * self.k_yx + ADC[1] * self.k_yy + self.y_offset,
                 self.z_scan())

    def calibrate(self):
        print("CALIBRATING TOUCH SCREEN.\n")

        filename = "RT_cal_coeffs.txt"

        try:
            with open(filename, 'r') as f:
                cal_data_string = f.readline()
                calib = [float(cal_value) for cal_value in cal_data_string.strip().split(',')]
                self.k_xx = calib[0]
                self.k_xy = calib[1]
                self.k_yx = calib[2]
                self.k_yy = calib[3]
                self.x_offset = calib[4]
                self.y_offset = calib[5]

        except:
            print("Follow instructions carefully!\n"
                  "Let center of touch screen be (0,0)")

            points = np.array([[0,0], [80, 40], [-80, 40], [-80, -40], [80, -40]])

            ADC = np.ones((5,3))

            for i in range(5):
                print("Touch point #{:}: ({:}, {:})".format(i, points[i,0], points[i,1]))
                while True:
                    if self.z_scan():
                        xy = self.xy_scan()
                        ADC[i,0] = xy[0]
                        ADC[i,1] = xy[1]
                        while True:
                            if not self.z_scan():
                                break
                        break

            # Calibration MATRIX MATH
            calib = np.dot(np.dot(np.linalg.inv(np.dot(ADC.transpose(), (ADC))), (ADC.transpose())), (points))

            self.k_xx = calib[0,0]
            self.k_yx = calib[0,1]
            self.k_xy = calib[1,0]
            self.k_yy = calib[1,1]
            self.x_offset = calib[2,0]
            self.y_offset = calib[2,1]

            with open(filename, 'w') as f:
                f.write(f"{self.k_xx}, {self.k_xy}, {self.k_yx}, {self.k_yy}, {self.x_offset}, {self.y_offset}\r\n")

        print("\nKxx: {:}, \tKyx: {:}\n"
              "Kxy: {:}, \tKyy: {:}\n"
              "Xc:  {:}, \tYc:  {:}\n".format(self.k_xx, self.k_yx, self.k_xy, self.k_yy, self.x_offset, self.y_offset))

        print("TOUCH SCREEN CALIBRATION COMPLETE!")

if __name__ == "__main__":

    '''@brief            instantiates touch panel attributes pin setup, panel dimensions, and origin offset
    '''
    panel = TouchDriver(Pin.cpu.C3, Pin.cpu.C0, Pin.cpu.C2, Pin.cpu.B0)
    panel.calibrate()

    while True:
        if panel.z_scan():
            start = utime.ticks_us()
            panel.scan_all()
            stop = utime.ticks_diff(utime.ticks_us(), start)
            print(str(stop) + " us")
            print("X: {:},\t Y: {:}".format(round(panel.x_scan()), round(panel.y_scan())))
    
