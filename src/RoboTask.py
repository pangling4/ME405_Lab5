''' @file       RoboTask.py
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

class RoboTask:
    '''! 
    This class implements a RoboBrain object to allow multitasking with the robot joints. 
    '''
    
    def __init__ (self, RoboBrain_obj, queue_x, queue_y, queue_th1, queue_th2, queue_th3):
        '''! 
        @brief                  Creates a RoboTask object
        @details                Controls operation of the robot with a FSM machine in the
                                run method which is used by a scheduler to control operation
                                of a parallel 3RR robot
        @param motor_const      A RoboBrain object which contains information about the geometry
                                of the robot.
        @param queue_x          The shares.Queue corresponding to finger x value on the touchpad
        @param queue_y          The shares.Queue corresponding to finger y value on the touchpad
        @param queue_th1        The shares.Queue corresponding to joint 1 theta value
        @param queue_th2        The shares.Queue corresponding to joint 2 theta value
        @param queue_th3        The shares.Queue corresponding to joint 3 theta value
        '''
        
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
        @details    Has states to calibrate the touch panel, calibrate the motors,
                    and continuously update the joint values for the robot
                    as a finger moves along the touchpad
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
                
            
            elif state == S1_CALIBRATE_TP:
                # Run touchpad calibration method
                # If touchpad is calibrated, transition to S2
                pass
            
            elif state == S2_CALIBRATE_MOT:
                # Run motor calibration method for each motor
                # If motors are calibrated, transition to S3
                pass
            
            elif state == S3_DRAW:
                
                # Update positions and move robot accordingly if there are positions waiting
                if self.x_queue.any():
                    
                    # Inverse kinematic calculation, arbitrarily set angle to 0 degrees
                    self.RoboBrain.update_joints(self.x_queue.get(), self.y_queue.get(), 0)
                    
                    # Update desired joint values for joint tasks
                    self.theta1_queue.put(self.RoboBrain.get_alpha1())
                    self.theta2_queue.put(self.RoboBrain.get_alpha2())
                    self.theta3_queue.put(self.RoboBrain.get_alpha3())
                    
                    # Solenoid.pen_down()
                    
                else:
                    # If no positions are waiting to be moved to, raise the solenoid
                    # Solenoind.pen_up()
                    pass
                
                # Always stays in drawing state until manually reset
            
            yield(state)
        
        
if __name__ == "__main__":
    pass
    
