import sys 
import warnings 
import time 
import keyboard 
from sympy import * 
import IK 
import IK_SceneSetup 
import KeyEvent 
from Robot import Robot 
from Scripts import Script 
 
sys.path.append("C:\Program Files\CoppeliaRobotics\CoppeliaSimEdu\programming\zmqRemoteApi\clients\python") 
from zmqRemoteApi import RemoteAPIClient 
 
init_printing(wrap_line=False) 
 
try: 
    client = RemoteAPIClient() 
    sim = client.getObject('sim') 
    simIK = client.getObject('simIK') 
 
    print(""" 
    DEMO 
    Welcome to the Coppeliasim interface demo - Inverse Kinematics 
    ------------------------------------------------------------------ 
 
    preparing the scene...\n 
    """) 
 
    Robot.import_robot('Franka') 
    franka = Robot('/Franka[0]') 
    bot = franka.get_name() 
    bot_handle = franka.get_bot() 
    end_effector = franka.get_end_effector() 
 
    # TIP AND TARGET 
    try: 
        simBase = franka.get_bot() 
        simTip = sim.getObject('/tip', {'noError': False}) 
        simTarget = sim.getObject('/target', {'noError': False}) 
    except Exception as e: 
        endPosition = sim.getObjectPosition(end_effector, bot_handle) 
        if not sim.isHandle(sim.getObjectHandle('/tip@silentError')) and not sim.isHandle(  
 
                sim.getObjectHandle('/target@silentError')): 
 
            tip = IK_SceneSetup.setup_tip(franka, endPosition) 
            target_dummy = IK_SceneSetup.setup_target(franka, endPosition) 
            IK_SceneSetup.link(tip, target_dummy) 
 
        elif sim.isHandle(sim.getObject('/tip@silentError')): 
            tip = sim.getObject('/tip') 
            target_dummy = IK_SceneSetup.setup_target(franka, endPosition) 
            IK_SceneSetup.link(tip, target_dummy) 
        elif sim.isHandle(sim.getObject('/target@silentError')): 
            target = sim.getObject('/target') 
            tip = IK_SceneSetup.setup_tip(franka, endPosition) 
            IK_SceneSetup.link(tip, target) 
        else: 
            warnings.warn("Error was detected:" + str(e) + "\nError couldn't be resolved. ") 
 
    finally: 
        simBase = bot_handle 
        simTip = sim.getObject('/tip', {'noError': False}) 
        simTarget = sim.getObject('/target', {'noError': False}) 
 
    # SCRIPTS 
    sim.removeScript(sim.getScript(sim.scripttype_childscript, bot_handle))  # remove old script 
    childHandle = Script('child', bot_handle) 
    childHandle.set_code("childScript_IK.txt") 
 
    graphHandle = Script('custom', bot_handle) 
    graphHandle.set_code("LUA_graph.txt") 
 
    print("\nSetup Complete\n") 
    print("Final Step requires manual interference. Please create 3 graphs in your current scene named:" 
          "CartesianPoints, JointAngles, EulerAngles\n\n" 
          "Once complete, press Enter") 
 
    while not keyboard.is_pressed('enter'):  # making a loop 
        pass 
 
    # MAIN FUNCTIONS 
    quitDemo = False 
    while not quitDemo: 
        print("""\n\n 
        1. Move the end-effector to an inputted cartesian position 
        2. Move the end_effector with Mouse 
        3. Control Panda with the keyboard\n 
        4. Quit Demo 
        """) 
        try: 
            opt = int(input("Out of the options above, which one do you want to try?\n--")) 
            if opt < 1 or opt > 4: 
                raise ValueError('Invalid input: please enter a number between 1 and 4') 
        except ValueError as e: 
            print(f"Error: {e}") 
            continue 
 
        graphHandle.init_script() 
        if opt == 1: 
            IK.move_to_cartesian_point(simBase, simTip, simTarget) 
 
        elif opt == 2: 
            manip_sphere = IK_SceneSetup.visible_sphere(simTarget)  
 
            print("Use the Mouse to drag the sphere to control robot Pose") 
            sim.startSimulation() 
 
            while not keyboard.is_pressed('esc'):  # making a loop 
                pass 
 
            sim.stopSimulation() 
            print("Mouse Drag control has stopped") 
            IK_SceneSetup.invisible_sphere(manip_sphere) 
 
        elif opt == 3: 
            KeyEvent.keyboard_control(simTip, simTarget) 
 
        elif opt == 4: 
            print("Thank you for trying the Demo") 
            quitDemo = True 
 
except Exception as e: 
    print(f"Error: {e}") 
    sys.exit(1)