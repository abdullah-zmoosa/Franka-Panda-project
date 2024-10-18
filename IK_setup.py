import sys 
 
from Robot import Robot 
 
sys.path.append("C:\Program Files\CoppeliaRobotics\CoppeliaSimEdu\programming\zmqRemoteApi\clients\python") 
from zmqRemoteApi import RemoteAPIClient  # despite showing error, it has access to the zmqAPI 
 
client = RemoteAPIClient() 
sim = client.getObject('sim') 
 
 
def enable_mode(joints: list, mode: str): 
    if mode.lower() == "dynamic": 
        [sim.setJointMode(joint, sim.jointmode_dynamic, 0) for joint in joints] 
    elif mode.lower() == "kinematic": 
        [sim.setJointMode(joint, sim.jointmode_kinematic, 0) for joint in joints] 
    elif mode.lower() == "dependant": 
        [sim.setJointMode(joint, sim.jointmode_dependent, 0) for joint in joints] 
    else: 
        print("Mode doesn't exist. Choose from either dynamic , kinematic or dependant") 
 
 
def setup_tip(robot: Robot, tip_position: list): 
    # Create tip 
    sim.createDummy(0.0100) 
 
 
    tip = sim.getObject("/Dummy") 
    if sim.isHandle(tip): 
        sim.setObjectAlias(tip, "tip") 
        sim.setObjectPosition(tip, robot.get_bot(), tip_position)   # move to end-effector position 
        sim.setObjectParent(tip, robot.get_end_effector(), True)    # make end-effector parent 
        return tip 
 
 
def setup_target(robot: Robot, tip_position: list): 
    # Create Target 
    sim.createDummy(0.0100) 
    target_dummy = sim.getObject("/Dummy") 
    if sim.isHandle(target_dummy): 
        sim.setObjectAlias(target_dummy, "target") 
        sim.setObjectPosition(target_dummy, robot.get_bot(), tip_position)  # move to tip position 
        sim.setObjectParent(target_dummy, robot.get_bot(), True)    # make robot the parent 
        return target_dummy 
 
 
def visible_sphere(target_dummy: int): 
    # create a manipulator sphere to give 'target' a shape 
    sim.createPrimitiveShape(sim.primitiveshape_spheroid, [0.05, 0.05, 0.05], 0) 
    manipulator = sim.getObject("/Sphere") 
    sim.setObjectAlias(manipulator, "manipulator") 
    sim.setShapeColor(manipulator, None, sim.colorcomponent_ambient_diffuse, [0, 0, 0.5]) 
    sim.setShapeColor(manipulator, None, sim.colorcomponent_transparency, [0.5]) 
    sim.setObjectPosition(manipulator, -1, sim.getObjectPosition(target_dummy, -1)) 
    sim.setObjectParent(manipulator, sim.getObjectParent(target_dummy), True) 
    sim.setObjectParent(target_dummy, manipulator, True)        # make sphere the parent of 'target' 
    return manipulator 
 
def invisible_sphere(manipHandle): 
    sim.removeObjects([manipHandle])        # remove(hide) the sphere 
 
 
def link(tip, target): 
    sim.setLinkDummy(tip, target) 