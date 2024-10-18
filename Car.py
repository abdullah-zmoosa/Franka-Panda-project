import math 
import sys 
import time 
 
import IK 
import IK_SceneSetup 
from Robot import Robot 
from Scripts import Script 
 
sys.path.append("C:\Program Files\CoppeliaRobotics\CoppeliaSimEdu\programming\zmqRemoteApi\clients\python") 
from zmqRemoteApi import RemoteAPIClient 
 
  
 
try: 
    client = RemoteAPIClient() 
    sim = client.getObject('sim') 
    simIK = client.getObject('simIK') 
 
    print(""" 
DEMO 
Welcome to the Coppeliasim interface demo - Inverse Kinematics 
------------------------------------------------------------------ 
 
preparing the scene...\n 
 
First: Ensure these objects are in the scene: tyre, car 
    """) 
 
    # tyre position can be anywhere as long as reachable by the robot end effector 
    tyre = sim.getObject('/Tyre') 
 
    # assuming the car position [+9.3500e-01, -7.4059e-01, +4.3000e-01] 
    # assuming the car orientation [+9.0000e+01, +2.0491e-05, +9.0000e+01] 
    car = sim.getObject('/Car') 
 
    franka = Robot('/Franka[0]') 
    bot_handle = franka.get_bot() 
    end_effector = franka.get_end_effector() 
    endPosition = sim.getObjectPosition(end_effector, bot_handle) 
 
    '''DUMMY SETUPS''' 
 
    # base robot tip and target dummies 
    tip = IK_SceneSetup.setup_tip(franka, endPosition) 
    target_dummy = IK_SceneSetup.setup_target(franka, endPosition) 
    IK_SceneSetup.link(tip, target_dummy) 
 
    simBase = bot_handle 
    simTip = sim.getObject('/tip') 
    simTarget = sim.getObject('/target') 
 
    # dummy for the tyre 
    tyre_waypoint = sim.createDummy(0.0100) 
    sim.setObjectAlias(tyre_waypoint, "tyre_waypoint") 
    sim.setObjectPosition(tyre_waypoint, -1, sim.getObjectPosition(tyre, 
sim.handle_world)) 
    sim.setObjectParent(tyre, tyre_waypoint, True) 
 
    # dummy waypoint for the final wheel insertion position and orientation 
    wheel_waypoint = sim.createDummy(0.0100) 
    sim.setObjectAlias(wheel_waypoint, "wheel_waypoint") 
    sim.setObjectPosition(wheel_waypoint, sim.handle_world, [+7.5000e-01, -1.1000e+00, 
+3.5000e-01]) 
    sim.setObjectOrientation(wheel_waypoint, -1, [+0.0000e+00, math.radians(-9.0000e+01), 
+0.0000e+00]) 
 
    '''SCRIPTS''' 
    sim.removeScript(sim.getScript(sim.scripttype_childscript, bot_handle))  # remove old script 
    childHandle = Script('child', bot_handle) 
    childHandle.set_code("childScript_IK.txt") 
 
    print("\nSetup Complete\n") 
 
    sim.startSimulation() 
 
    # end-effector goes to tyre position 
    IK.move_to_cartesian_point(simBase, simTip, simTarget, tyre_waypoint) 
 
 
 
    # robot picks up wheel 
    sim.setObjectParent(tyre_waypoint, sim.getObjectParent(franka.get_end_effector())) 
 
    # carry the tyre to the final position 
    IK.move_to_cartesian_point(simBase, tyre_waypoint, simTarget, wheel_waypoint) 
    time.sleep(3) 
 
    sim.stopSimulation() 
 
except Exception as e: 
    print(f"Error: {e}") 
    sys.exit(1) 