## @file mainpage.py
# @author Jonathan Cederquist, Tim Jain, Philip Pang
# @mainpage Term Project
# @section intro_sec Software Design
# @subsection ss_FSM Finite State Machine
# @image html RobotFSM.png State Transition Diagram
# The finite state machine is very simple. Although this design is not very
# robust, it reflects the state of our code when the robot was tested.
# The calibration for the touchpad and the encoders (finding a known angle)
# occurs in the main.py file when each task is created. The constructor for
# jointTask and taskTouch each runs the calibrate method when a task is created
# which either reads from a file with given constants or asks for user input
# to calibrate the device. After the calibration for the touch pad and 3 links
# is complete, the task scheduler begins running. This finite state machine is
# found in the run method of roboTask, the "brain" task which interfaces between
# the touchpad user position and the inverse kinematics to provide angles for each
# of the joint (motor, encoder, controller) tasks.
# 
# S0 is the initialization state where all shared variables are reset. After this has
# been completed, the roboTask immediately transitions to S3 DRAWING, which runs the
# normal drawing operation for the robot. In this state, the brain checks whether any
# positions have been added to the x and y queues, then runs the inverse kinematics
# and updates the joint angles accordingly. If there are no positions to move to, the
# robot lifts the solenoid and waits until the queue is populated. The ready flag controls
# the end of the robot motion. When the program is exited, the ready flag is flippped,
# which stops the motors and solenoid.
#
# @subsection ss_Task Task Diagram
# We decided to combine the motor, encoder, and closed loop controller tasks
# within one task for each motor system. This creates three tasks, in which the 
# respective joint angles are being sent from the robot task, which computes
# the inverse kinematics of the 3R joint parallel robot. Additionally, there is
# a touch task that corresponds to the user touching the touch pad, drawing
# with their finger. Their motions are stored positionally within queues. 
# @image html TaskDiagram.png Task Diagram
