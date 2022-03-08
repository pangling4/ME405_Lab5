''' @file       RoboBrain.py
    @brief      Used to coordinate kinematics of 3 RRR robot
    @details    Implements inverse kinematic equations for a 3 RRR planar
                parallel robot
    @author     Jonathan Cederquist
    @author     Tim Jain
    @author     Philip Pang
    @date       Last Modified 2/25/22
'''

import math

class RoboBrain:
    '''! 
    This class facilitates kinematics for a 3 RRR planar parallel robot. 
    '''
    
    def __init__ (self, joint1loc, joint2loc, joint3loc, alength, blength,
                  c1, c2, c3, dbg_Flag=False):
        '''! 
        @brief              Creates a RoboBrain object
        @details            Creates a RoboBrain object by saving relevant geometric
                            parameters and initializing all location variables
        @param joint1loc    A column or row vector (list) of floats describing
                            the (x, y) location of joint 1 relative to the universal
                            coordinate frame origin. Ex: joint1loc = [5.33, 2.4]
                            Units are expected to be in inches
        @param joint2loc    A column or row vector (list) of floats describing
                            the (x, y) location of joint 2 relative to the universal
                            coordinate frame origin in units of inches
        @param joint3loc    A column or row vector (list) of floats describing
                            the (x, y) location of joint 3 relative to the universal
                            coordinate frame origin in units of inches
        @param alength      The length of the driven arm for each joint. If alength
                            is a single value, it is assumed that each link is
                            symmetrical. If alength is a list, RoboBrain will assume
                            the a lengths are given as [a1, a2, a3]. Units are
                            expected to be in inches, type float
        @param blength      The length of the passive arm for each joint. If blength
                            is a single value, it is assumed that each link is
                            symmetrical. If blength is a list, RoboBrain will assume
                            the a lengths are given as [b1, b2, b3]. Units are
                            expected to be in inches, type float
        @param c1           A column or row vector (list) of floats describing
                            the (x, y) location of attachment point C1 relative
                            to the center of the moving platform P when the robot
                            is in the reset position. Units are expected in inches
        @param c2           A column or row vector (list) of floats describing
                            the (x, y) location of attachment point C2 relative
                            to the center of the moving platform P when the robot
                            is in the reset position. Units are expected in inches
        @param c3           A column or row vector (list) of floats describing
                            the (x, y) location of attachment point C3 relative
                            to the center of the moving platform P when the robot
                            is in the reset position. Units are expected in inches
        '''
        
        # Save joint locations
        self.l1 = joint1loc
        self.l2 = joint2loc
        self.l3 = joint3loc
        
        # Check if a and b lengths are specified as unique, then save accordingly
        if isinstance(alength, list):
            self.a1 = alength[0]
            self.a2 = alength[1]
            self.a3 = alength[2]
        else:
            self.a1 = alength
            self.a2 = alength
            self.a3 = alength
        
        if isinstance(blength, list):
            self.b1 = blength[0]
            self.b2 = blength[1]
            self.b3 = blength[2]
        else:
            self.b1 = blength
            self.b2 = blength
            self.b3 = blength
        
        # Save platform attachment (C) locations
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        
        # Location and orientation of platform center
        self.P = [0, 0]
        self.theta = 0
        
        self.dbg_Flag = dbg_Flag
        
        # Joints angles
        self.alpha1 = 0.0
        self.alpha2 = 0.0
        self.alpha3 = 0.0
        
        # Initialize other useful geometry variables
        self.prevP = [0, 0]
        self.prevTheta = 0
        
        self.prevAlpha1 = 0
        self.prevAlpha2 = 0
        self.prevAlpha3 = 0
        
    
    def reset(self):
        '''!
        @brief Resets the position of the robot to (0,0) at orientation 0
        '''
        
        self.P = [0, 0]
        self.theta = 0
        
        
    def get_position(self):
        '''!
        @brief Returns the current position of the robot
        '''
        
        return self.P
    
    def get_theta(self):
        '''!
        @brief Returns the current orientation of the robot
        '''
        
        return self.theta
    
    def get_x(self):
        '''!
        @brief Returns the current x-coordinate of the robot
        '''
        
        return self.P[0]
    
    def get_y(self):
        '''!
        @brief Returns the current y-coordinate of the robot
        '''
        
        return self.P[1]
    
    def set_position(self, newX, newY):
        '''!
        @brief      Sets the robot position to [newX, newY]
        @param newX The new x-coordinate of the position
        @param newY The new y-coordinate of the position
        '''
        
        self.prevP = self.P
        self.P[0] = newX
        self.P[1] = newY
        
    def set_x(self, newX):
        '''!
        @brief      Sets the robot x position to newX
        @param newX The new x-coordinate of the position
        '''
        
        self.prevP = self.P
        self.P[0] = newX
    
    def set_y(self, newY):
        '''!
        @brief      Sets the robot y position to newY
        @param newY The new y-coordinate of the position
        '''
        
        self.prevP = self.P
        self.P[1] = newY
    
    def set_theta(self, newTheta):
        '''!
        @brief          Sets the robot orientation to newTheta
        @param newTheta The new orientation of the robot
        '''
        
        self.prevTheta = self.theta
        self.theta = newTheta
    
    def update_joints(self, newX, newY, newTheta):
        '''!
        @brief          Updates the joint values of the robot 
        @details        Uses inverse kinematic equations derived from Introduction
                        to Robotics: Analysis, Control, Application 3rd Ed by
                        Saeed B. Niku to calculate the necessary angles alpha1,
                        alpha2, and alpha3 for the given position and orientation
        @param newX     The desired x-coordinate to move the robot to
        @param newY     The desired y-coordinate to move the robot to
        @param newTheta The desired orientation to move the robot to
        '''
        
        # Update position and orientation
        self.set_position(newX, newY)
        self.set_theta(newTheta)
        
        # Save previous joint values for trajectory decisions
        self.prevAlpha1 = self.alpha1
        self.prevAlpha2 = self.alpha2
        self.prevAlpha3 = self.alpha3
        
        # Calculate alpha values for each joint
        
        # Joint 1
        q1x = self.l1[0] -self.P[0] - self.c1[0]*math.cos(math.radians(self.theta))\
              + self.c1[1]*math.sin(math.radians(self.theta))
        
        q1y = self.l1[1] -self.P[1] - self.c1[0]*math.sin(math.radians(self.theta))\
              - self.c1[1]*math.cos(math.radians(self.theta))
        
        Q1 = (self.b1**2 - self.a1**2 - q1x**2 -q1y**2)/(2*self.a1)
        
        denom = (q1x**2 + q1y**2)**0.5
        
        if self.dbg_Flag:
            print("q1x = ", q1x)
            print("q1y = ", q1y)
            print("Q1 = ", Q1)
            
        omega = math.degrees(math.atan2(q1x/denom, q1y/denom))
        
        if self.dbg_Flag:
            print("Omega = ", omega)
            
        alf = math.degrees(math.asin(Q1/denom))
        
        alpha1_1 = alf - omega
        alpha1_2 = (180-alf) - omega
        
        # Adjust joint options so angle is always between 0 and 360
        while (alpha1_1 < 0) or (alpha1_1 >= 360):
            if alpha1_1 < 0:
                alpha1_1 += 360
            elif alpha1_1 >= 360:
                alpha1_1 -= 360
        
        while (alpha1_2 < 0) or (alpha1_2 >= 360):
            if alpha1_2 < 0:
                alpha1_2 += 360
            elif alpha1_2 >= 360:
                alpha1_2 -= 360
                
        if self.dbg_Flag:
            print("Alpha1, option 1 = ", alpha1_1)
            print("Alpha1, option 2 = ", alpha1_2)
            
        # Determine correct 'delta' values
        delta1_1 = abs(alpha1_1-self.prevAlpha1)
        
        if delta1_1 > 180:
            delta1_1 = abs(alpha1_1-self.prevAlpha1-360)
        
        delta1_2 = abs(alpha1_2-self.prevAlpha1)
        
        if delta1_2 > 180:
            delta1_2 = abs(alpha1_2-self.prevAlpha1-360)
        
        # Set alpha 1 to joint value that is closest to previous
        if(delta1_1 < delta1_2):
            self.alpha1 = alpha1_1
        else:
            self.alpha1 = alpha1_2
        
        # Joint 2
        q2x = self.l2[0] -self.P[0] - self.c2[0]*math.cos(math.radians(self.theta))\
              + self.c2[1]*math.sin(math.radians(self.theta))
        
        q2y = self.l2[1] -self.P[1] - self.c2[0]*math.sin(math.radians(self.theta))\
              - self.c2[1]*math.cos(math.radians(self.theta))
        
        Q2 = (self.b2**2 - self.a2**2 - q2x**2 -q2y**2)/(2*self.a2)
        
        denom2 = (q2x**2 + q2y**2)**0.5
        
        if self.dbg_Flag:
            print("q2x = ", q2x)
            print("q2y = ", q2y)
            print("Q2 = ", Q2)
            
        omega2 = math.degrees(math.atan2(q2x/denom2, q2y/denom2))
        
        if self.dbg_Flag:
            print("Omega2 = ", omega2)
            
        alf2 = math.degrees(math.asin(Q2/denom2))
        
        alpha2_1 = alf2 - omega2
        alpha2_2 = (180-alf2) - omega2
        
        # Adjust joint options so angle is always between 0 and 360
        while (alpha2_1 < 0) or (alpha2_1 >= 360):
            if alpha2_1 < 0:
                alpha2_1 += 360
            elif alpha2_1 >= 360:
                alpha2_1 -= 360
        
        while (alpha2_2 < 0) or (alpha2_2 >= 360):
            if alpha2_2 < 0:
                alpha2_2 += 360
            elif alpha2_2 >= 360:
                alpha2_2 -= 360
                
        if self.dbg_Flag:
            print("Alpha2, option 1 = ", alpha2_1)
            print("Alpha2, option 2 = ", alpha2_2)
            
        # Determine correct 'delta' values
        delta2_1 = abs(alpha2_1-self.prevAlpha2)
        
        if delta2_1 > 180:
            delta2_1 = abs(alpha2_1-self.prevAlpha2-360)
        
        delta2_2 = abs(alpha2_2-self.prevAlpha2)
        
        if delta2_2 > 180:
            delta2_2 = abs(alpha2_2-self.prevAlpha2-360)
        
        # Set alpha 2 to joint value that is closest to previous
        if(delta2_1 < delta2_2):
            self.alpha2 = alpha2_1
        else:
            self.alpha2 = alpha2_2
        
        # Joint 3
        q3x = self.l3[0] -self.P[0] - self.c3[0]*math.cos(math.radians(self.theta))\
              + self.c3[1]*math.sin(math.radians(self.theta))
        
        q3y = self.l3[1] -self.P[1] - self.c3[0]*math.sin(math.radians(self.theta))\
              - self.c3[1]*math.cos(math.radians(self.theta))
        
        Q3 = (self.b3**2 - self.a3**2 - q3x**2 -q3y**2)/(2*self.a3)
        
        denom3 = (q3x**2 + q3y**2)**0.5
        
        if self.dbg_Flag:
            print("q3x = ", q3x)
            print("q3y = ", q3y)
            print("Q3 = ", Q3)
            
        omega3 = math.degrees(math.atan2(q3x/denom3, q3y/denom3))
        
        if self.dbg_Flag:
            print("Omega3 = ", omega3)
            
        alf3 = math.degrees(math.asin(Q3/denom3))
        
        alpha3_1 = alf3 - omega3
        alpha3_2 = (180-alf3) - omega3
        
        # Adjust joint options so angle is always between 0 and 360
        while (alpha3_1 < 0) or (alpha3_1 >= 360):
            if alpha3_1 < 0:
                alpha3_1 += 360
            elif alpha3_1 >= 360:
                alpha3_1 -= 360
        
        while (alpha3_2 < 0) or (alpha3_2 >= 360):
            if alpha3_2 < 0:
                alpha3_2 += 360
            elif alpha3_2 >= 360:
                alpha3_2 -= 360
                
        if self.dbg_Flag:
            print("Alpha3, option 1 = ", alpha3_1)
            print("Alpha3, option 2 = ", alpha3_2)
            
        # Determine correct 'delta' values
        delta3_1 = abs(alpha3_1-self.prevAlpha3)
        
        if delta3_1 > 180:
            delta3_1 = abs(alpha3_1-self.prevAlpha3-360)
        
        delta3_2 = abs(alpha3_2-self.prevAlpha3)
        
        if delta3_2 > 180:
            delta3_2 = abs(alpha3_2-self.prevAlpha3-360)
        
        # Set alpha 2 to joint value that is closest to previous
        if(delta3_1 < delta3_2):
            self.alpha3 = alpha3_1
        else:
            self.alpha3 = alpha3_2
        
    def get_alpha1(self):
        '''!
        @brief Returns the value (in degrees) of alpha1 (angle of joint 1)
        '''
        return self.alpha1
    
    def get_alpha2(self):
        '''!
        @brief Returns the value (in degrees) of alpha2 (angle of joint 2)
        '''
        return self.alpha2
    
    def get_alpha3(self):
        '''!
        @brief Returns the value (in degrees) of alpha3 (angle of joint 3)
        '''
        return self.alpha3
    
        
if __name__ == "__main__":
    myRoboBrain = RoboBrain([0, 0], [10, 0], [5, 8.66], 4, 4, [-1.5, -0.866],\
                            [1.5, -0.866], [0, 1.73], dbg_Flag=True)
    myRoboBrain.set_x(7)
    print("After setting x to 7, x is:", myRoboBrain.get_x())
    
    myRoboBrain.set_y(5)
    print("After setting y to 5, y is:", myRoboBrain.get_y())
    
    myRoboBrain.reset()
    print("After resetting position, position is: ", myRoboBrain.get_position())
    
    myRoboBrain.update_joints(7, 5, 0)
    print("After updating joints for P = (7, 5), theta = 0 degrees")
    print("Alpha 1 = ", myRoboBrain.get_alpha1())
    print("Alpha 2 = ", myRoboBrain.get_alpha2())
    print("Alpha 3 = ", myRoboBrain.get_alpha3())
    
    
    
    