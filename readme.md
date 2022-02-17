# Term Project: 2.5 Axis Machine
Our group is planning to use a 3-RRR planar parallel robot for this
project. Using our knowledge from robotics, along with a helpful
research paper from Vanderbilt, we already have known equations for the
inverse kinematics. The advantage of using a parallel robot is that
the actuators are stationary and the inverse kinematics are much
simpler than in a serial robot. A generic representation of a planar
3-RRR parallel robot is shown below in Figure 1.

![3-RRR Planar Parallel Robot!](rrr_robot.png)

*Figure 1: Schematic for a generic 3-RRR Planar Parallel Robot.*

Since we do not care about the orientation of the 'pen', we can simply
arbitrarily always set the angle at some constant value and then solve
for the angles necessary to move the base platform to the desired
location. Our plan is to use scrap metal from the ME 405 Lab for all
the links as well as the baseplate. We will also use scrap MDF from the
ME 405 Lab as a base for motors and links to be mounted on.
In order to actuate the driven links, we will use ??? motors with
encoders to faciliate closed loop position control. The pen's machining
operation will be turned 'on'/'off' using a solenoid. The connections
between links and the drawing platform will use ?bushings? to allow
for low friction rotation.

## Preliminary Bill of Materials
The following table shows the preliminary bill of materials for our
machine. Minor components such as hardware and wires are not included.

| Qty. | Part                     | Source                | Est. Cost |
|:----:|:-------------------------|:----------------------|:---------:|
|  3   | Pittperson Gearmotors    | ME405 Tub             |     -     |
|  1   | Nucleo with Shoe         | ME405 Tub             |     -     |
|  6   | Aluminum Link            | ME405 Scrap Bin       |     -     |
|  1   | Aluminum Draw Plate      | ME405 Scrap Bin       |     -     |
|  1   | 2'x 2' MDF Base Plate    | Home Depot            |  $14.73   |
|  1   | Black Ultra Fine Sharpie | Staples (5-pack)      |   $5.79   |

## Preliminary CAD
Below, we have included rough 2D and 3D models showing the proposed
arrangement of our machine.


