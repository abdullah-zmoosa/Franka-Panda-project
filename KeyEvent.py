import keyboard  # used for keyboard control 
import sys 
import time 
 
sys.path.append("C:\ProgramFiles\CoppeliaRobotics\CoppeliaSimEdu\programming\zmqRemoteApi\clients\python") 
from zmqRemoteApi import RemoteAPIClient 
 
client = RemoteAPIClient() 
sim = client.getObject('sim') 
 
 
# start the simulation and show the user the instructions for the keyboard movement 
def keyboard_control(tipHandle: int, targetHandle: int): 
    print(""" 
    Q - increments by 0.005m in the positive x direction 
    A - decrements by 0.005m in the negative x direction 
    W - increments by 0.005m in the positive y direction 
    S - decrements by 0.005m in the negative y direction 
    E - increments by 0.005m in the positive z direction 
    D - decrements by 0.005m in the negative z direction 
    """) 
 
    sim.startSimulation() 
 
    matrix = []  # initializes a matrix variable 
 
    while not keyboard.is_pressed('esc'):  # making a loop 
 
        start = sim.getObjectPose(tipHandle, -1) 
        matrix = start 
 
        # time.sleep(0.00)  
 
        # initializes what each key does for the manipulation of position and updates the matrix variable 
 
        keyboard.block_key('q') 
        keyboard.block_key('a') 
        keyboard.block_key('w') 
        keyboard.block_key('s') 
        keyboard.block_key('e') 
        keyboard.block_key('d') 
        if keyboard.is_pressed('q'): 
            matrix[0] += 0.005 
        elif keyboard.is_pressed('a'): 
            matrix[0] -= 0.005 
        elif keyboard.is_pressed('w'): 
            matrix[1] += 0.005 
        elif keyboard.is_pressed('s'): 
            matrix[1] -= 0.005 
        elif keyboard.is_pressed('e'): 
            matrix[2] += 0.005 
        elif keyboard.is_pressed('d'): 
            matrix[2] -= 0.005 
        else: 
            pass 
 
        sim.setObjectPose(targetHandle, -1, 
                          matrix)  # sets the position of the manipulator to the target position updated by matrix 
 
    sim.stopSimulation()  # stops the simulation when esc is pressed 
 
    print("Keyboard control has stopped")