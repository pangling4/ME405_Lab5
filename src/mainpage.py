## @file mainpage.py
# @author Jonathan Cedarquist, Tim Jain, Philip Pang
# @mainpage Term Project
# @section intro_sec Software Design
# @subsection ss_FSM Finite State Machine
# @image html 3R_FSM_Touch.drawio.png Finite State Diagram
# The finite state machine involves first calibrating the touch sensor. This
# is done by touching the touch pad at various points and ensuring that those
# locations align correctly. Then, it transitions to calibrating the motors. 
# This calibrates one motor at a time by running the motor until it has hit 
# its limit switch that is attached to each link. Then, it transitions to 
# activating the solenoid and lowering the pen holder to touch the paper if a
# touch signal is given. 
# When it touches the paper as the user is touching the touch pad, the drawing
# sequence is performed, moving the links based on the inverse kinematics of 
# the robot task, and moving the motors at appropriate speeds based on closed 
# loop control. When the user removes their finger from the touch pad, the 
# solenoid pulls, raising the pen. States 3, 4, and 5 are repeated until the 
# program is halted.
# @subsection ss_Task Task Diagram
# We decided to combine the motor, encoder, and closed loop controller tasks
# within one task for each motor system. This creates three tasks, in which the 
# respective joint angles are being sent from the robot task, which computes
# the inverse kinematics of the 3R joint parallel robot. Additionally, there is
# a solenoid task for the raising and lowering of the pen, and a user interface
# task. The touch task corresponds to the user touching the touch pad, drawing
# with their finger. Their motions are stored positionally within queues. 
# @image html TaskDiagram.png Task Diagram
