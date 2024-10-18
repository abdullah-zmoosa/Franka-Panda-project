# Robotic Manipulator Simulation with CoppeliaSim

This project simulates a robotic manipulator using CoppeliaSim and Python. The goal is to control and analyze the movement of the Franka Panda robot arm in a virtual environment. The implementation is done using Python API, making use of the ZEROMQ interface to communicate with CoppeliaSim. The project covers various tasks involving Cartesian positioning, velocity control, and trajectory planning for the robot arm.

## Features

- **Control End-Effector Position**: Move the robot's end effector to any Cartesian position using mouse control or input coordinates.
- **Velocity Control**: Set custom translational and rotational velocities for smooth manipulator movement.
- **Trajectory Following**: Utilize the Ruckig trajectory generator to make the robot follow a specified path automatically.
- **Joint Angles & End-Effector Tracking**: Read, write, and plot the robot's joint angles, Cartesian coordinates, and Euler angles.
- **Jacobian Calculation**: Compute and output the manipulator's Jacobian matrix.
- **Keyboard Controls**: Move the robot using keyboard inputs, providing intuitive manual control over each axis.

## Technology Stack

- **Software**: CoppeliaSim for 3D simulation
- **Programming Language**: Python (using ZEROMQ API for communication)
- **Robot Model**: Franka Emika Panda
- **Trajectory Generation**: Ruckig online trajectory generator

## Setup & Installation

1. **Dependencies**:
   - Python 3.x
   - CoppeliaSim (Educational version)
   - Python libraries: `zmq`, `cbor`, `keyboard`, `sympy`

2. **Connecting CoppeliaSim with Python**:
   - Make sure CoppeliaSim is running.
   - Use ZEROMQ API to connect your Python environment with CoppeliaSim.
   - The `zmqRemoteApi` library must be in your Python path to allow interaction.

3. **Running the Project**:
   - Clone the project and navigate to the directory.
   - Run the main interface script `main.py` to start controlling the robot.
   - Follow the prompts to choose between different control modes (mouse, Cartesian position, keyboard control).

## Usage Instructions

- **Mouse Control**: Drag the sphere linked to the end effector to manipulate the arm in real time.
- **Cartesian Coordinates**: Enter desired (x, y, z) coordinates and velocities to position the arm accordingly.
- **Keyboard Control**: Use pre-defined keys to control movement in real-time:
  - `Q/A` for x-axis movements
  - `W/S` for y-axis movements
  - `E/D` for z-axis movements
- **Trajectory Following**: Input a target position to initiate automatic path following.

## Files Overview

- **`main.py`**: Main script to set up and control the robotic manipulator using various modes.
- **`IK.py`**: Contains the inverse kinematics functions used to calculate the necessary transformations for positioning.
- **`KeyEvent.py`**: Handles keyboard-based control of the robot.
- **`IK_setup.py`**: Utility functions for setting up the environment, including dummy objects used for IK.
- **`Child Script_IK.lua` and `LUA_graph.lua`**: Embedded scripts for graphing joint angles and end-effector positions in CoppeliaSim.
- **`Car.py`**: Demonstrates a practical example where the robot arm picks up and places a wheel on a car body.

## Known Issues

- The current implementation assumes perfect conditions in CoppeliaSim. Calibration and positioning issues might arise with different 3D models or environments.
- The Ruckig trajectory generation is limited by its real-time constraints, which may not always provide a smooth path for sudden coordinate changes.

