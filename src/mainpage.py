## @file mainpage.py
# @author Jonathan Cedarquist, Tim Jain, Philip Pang
# @mainpage Term Project
# @section intro_sec Software Design
# @subsection ss_FSM Finite State Machine
# @image html 3R_FSM_Touch.drawio.png Finite State Diagram
# The finite state machine first involves calibration. Before calibrating,
# the RoboTask is initialized and also activates the solenoid, lifting up the
# pen. Next is the touch screen calibration. If a calibration file exists, then
# the calibration procedure does not need to be performed. If not, the procedure
# is done by touching the touch pad at set points and calculating angle and
# scale biases that those that the touches might reveal. Then, the FSM transitions
# to calibrating the motors. A message is shown in the console to prompt the
# user to manually move the linkages of the robot, one arm at a time. The limit
# switch will run over a ramp once in an arbitrary direction and back over a
# second time in the opposite direction. The calibration code will read these
# limit switch signals and will set the encoder values in the motor to their
# respective correct values that were hand measured when building the robot.
# Finally, all communication queues that contain touch tracking and position data
# are cleared.
# 
# In the second state, the drawing executes if the robot is ready and if contact
# is made on the touch panel.
# When it touches the paper as the user is touching the touch pad, the drawing
# sequence is performed, letting the pen down to draw and moving the links based
# on the inverse kinematics of 
# the robot task, and moving the motors at appropriate speeds based on closed 
# loop control. When the user removes their finger from the touch pad, the 
# solenoid pulls, raising the pen. States 1 and 2 are repeated until the 
# program is halted.
# @subsection ss_Task Task Diagram
# We decided to combine the motor, encoder, and closed loop controller tasks
# within one task for each motor system. This creates three tasks, in which the 
# respective joint angles are being sent from the robot task, which computes
# the inverse kinematics of the 3R joint parallel robot. Additionally, there is
# a touch task that corresponds to the user touching the touch pad, drawing
# with their finger. Their motions are stored positionally within queues. 
# @image html TaskDiagram.png Task Diagram
