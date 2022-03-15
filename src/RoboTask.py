'''!
@file       RoboTask.py
@brief      Facilitates multitasking with for the RoboBrain
@details    Contains a FSM which controls the operation of a parallel 3RRR
            robot. The run method is used by the cotask scheduler to continuously
            update the desired angles from the inverse kinematics
@author     Jonathan Cederquist
@author     Tim Jain
@author     Philip Pang
@date       Last Modified 3/7/22
'''

S0_INIT = 0
S1_CALIBRATE_TP = 1
S2_CALIBRATE_MOT = 2
S3_DRAW = 3

import pyb
import RoboSolenoidDriver

class RoboTask:
    '''! 
    This class implements a RoboBrain object to allow multitasking with the robot joints. 
    '''
    
    def __init__ (self, ready, RoboBrain_obj, queue_x, queue_y, queue_th1, queue_th2, queue_th3):
        '''! 
        @brief                  Creates a RoboTask object
        @details                Controls operation of the robot with a FSM machine in the
                                run method which is used by a scheduler to control operation
                                of a parallel 3RR robot
        @param ready            A task_share.Share used to stop operation when the robot is shut
                                down.
        @param RoboBrain_obj    A RoboBrain object which contains information about the geometry
                                of the robot.
        @param queue_x          The task_share.Queue corresponding to finger x value on the touchpad
        @param queue_y          The task_share.Queue corresponding to finger y value on the touchpad
        @param queue_th1        The task_share.Queue corresponding to joint 1 theta value
        @param queue_th2        The task_share.Queue corresponding to joint 2 theta value
        @param queue_th3        The task_share.Queue corresponding to joint 3 theta value
        '''
        self.ready = ready
        pinA8 = pyb.Pin(pyb.Pin.board.PA8, pyb.Pin.OUT_PP)
        pinB10 = pyb.Pin(pyb.Pin.board.PB10, pyb.Pin.OUT_PP)
    
        self.solenoid = RoboSolenoidDriver.RoboSolenoidDriver(pinA8, pinB10, 2, 3)
        self.solenoid.pull_up()

    
        # Create RoboBrain object used to calculate inverse kinematics
        self.RoboBrain = RoboBrain_obj
        
        # Create variables to access queue of position values
        self.x_queue = queue_x
        self.y_queue = queue_y
        
        # Create variables to access queues of joint angle values
        self.theta1_queue = queue_th1
        self.theta2_queue = queue_th2
        self.theta3_queue = queue_th3
        
    def run(self):
        '''!
        @brief      Generator FSM which controls operation of the robot
        @details    Initializes the shared variables, then continuously updates
                    the joint values for the robot as a finger moves along the touchpad.
                    Calibration is done in the main file when tasks are created.
        '''
        
        state = S0_INIT
        
        while True:
            
            if state == S0_INIT:
                # Reset all queues
                self.x_queue.clear()
                self.y_queue.clear()
                self.theta1_queue.clear()
                self.theta2_queue.clear()
                self.theta3_queue.clear()
                state = S3_DRAW
            
            elif state == S1_CALIBRATE_TP:
                # Run touchpad calibration method
                # If touchpad is calibrated, transition to S2
                pass
            
            elif state == S2_CALIBRATE_MOT:
                # Run motor calibration method for each motor
                # If motors are calibrated, transition to S3
                pass
            
            elif state == S3_DRAW:
                if self.ready.get() == 0:
                    self.solenoid.push_down()
                    print("Stop supplying power to solenoid")
                # Update positions and move robot accordingly if there are positions waiting
                elif self.x_queue.any():
                    
                    self.solenoid.push_down()
                    # Inverse kinematic calculation, arbitrarily set angle to 0 degrees
                    x = self.x_queue.get()
                    y = self.y_queue.get()
                    self.RoboBrain.update_joints(x, y, 0)
                    
                    # Update desired joint values for joint tasks
                    self.theta1_queue.put(self.RoboBrain.get_alpha1())
                    print("x: " + str(x) + "     y: "+ str(y))
                    print("theta1:" + str(self.RoboBrain.get_alpha1()))
                    self.theta2_queue.put(self.RoboBrain.get_alpha2())
                    print("theta2:" + str(self.RoboBrain.get_alpha2()))
                    self.theta3_queue.put(self.RoboBrain.get_alpha3())
                    print("theta3:" + str(self.RoboBrain.get_alpha3()))
                                        
                else:
                    # If no positions are waiting to be moved to, raise the solenoid
                    self.solenoid.pull_up()
                    #pass
                
                # Always stays in drawing state until manually reset
            print(state)
            yield(state)
        
if __name__ == "__main__":
    pass
    

