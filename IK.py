import sys, os 
 
sys.path.append("C:\Program Files\CoppeliaRobotics\CoppeliaSimEdu\programming\zmqRemoteApi\clients\python") 
from zmqRemoteApi import RemoteAPIClient  # despite showing error, it has access to the zmqAPI 
 
from sympy import * 
 
 
init_printing(wrap_line=False) 
 
client = RemoteAPIClient() 
sim = client.getObject('sim') 
simIK = client.getObject('simIK') 
 
maxJerk = 80  # setting as a constant value 
 
 
def cb(pose, vel, accel, handle): 
    sim.setObjectPose(handle, -1, pose) 
 
# move the tip of the manipulator to a given Cartesian target point 
def move_to_pose(init_Pose, maxVel, maxAccel, target_Pose, targetHandle): 
    sim.moveToPose(-1, init_Pose, [maxVel], [maxAccel], [maxJerk], target_Pose, cb, 
targetHandle, [1, 1, 1, 0.1]) 
 
# return a transformation matrix given coordinates and Euler angles 
def get_trans_matrix(coords, euler_angles): 
    return sim.buildMatrix(coords, euler_angles) 
 
#return the position given a transformation matrix 
def get_pose_from_matrix(transMatrix): 
    return sim.matrixToPose(transMatrix) 
 
#compute and return the Jacobian matrix 
def getJacobian(simBase): 
    scripthandle = sim.getScript(sim.scripttype_childscript, simBase) 
    matrix, size = sim.callScriptFunction('Jacobian', scripthandle) 
    # The number of rows equals the number of degrees of freedom in the Cartesian space being considered. The number 
    # of columns in a Jacobian is equal to the number of joints of the manipulator. 
    jacobian = Matrix(size[0], size[1], matrix) 
    print(size) 
    pprint(jacobian.transpose()) 
    return jacobian 
 
# allow the user to enter the target Cartesian point and Euler angles for the target pose as well as the maximum velocity and acceleration of the manipulator 
def get_mov_data(simTip, simTarget): 
    initialPose = sim.getObjectPose(simTip, -1) 
    print("Enter in the Cartesian Position of the target. The values should be <0.1, since the metric system is meters") 
    targetX = float(input("X: ")) 
    targetY = float(input("Y: ")) 
    targetZ = float(input("Z: ")) 
 
    print("Now enter the Euler Angles if a factor. If not, you can set them to 0") 
    eulerX = float(input("Angle X: ")) 
    eulerY = float(input("Angle Y: ")) 
    eulerZ = float(input("Angle Z: ")) 
 
    targetPose = get_pose_from_matrix(get_trans_matrix([targetX, targetY, targetZ], 
[eulerX, eulerY, eulerZ])) 
 
    maxVel = float(input("Enter the velocity of the bot joints : ")) 
    maxAccel = float(input("Enter the acceleration of the bot joints (Please keep the value <=1): ")) 
 
    mov_Data = { 
        'Handle': simTarget, 
        'initialPose': initialPose, 
        'targetPose': targetPose, 
        'maxVel': maxVel, 
 
        'maxAccel': maxAccel 
    } 
 
    return mov_Data 
 
#start the simulation and allows the user to output the jacobian matrix after the simulation is over 
def move_to_cartesian_point(baseHandle, tipHandle, targetHandle): 
    sim.startSimulation() 
 
    movementData = get_mov_data(tipHandle, targetHandle) 
 
    move_to_pose(movementData.get('initialPose'), movementData.get('maxVel'), 
movementData.get('maxAccel'), 
                 movementData.get('targetPose'), movementData.get('Handle')) 
 
    ask_jaco = input("Do you want to see the resulting Jacobian Matrix? y/n : ") 
    if ask_jaco.lower() == 'y': 
        jacobian_matrix = getJacobian(baseHandle) 
 
    sim.stopSimulation()