#python  
 
def Jacobian(): 
    if(simIK.computeJacobian(ikEnv,ikGroup, 0)): 
        jacobian, jacobian_size = simIK.getJacobian(ikEnv,ikGroup, 0) 
        return jacobian, jacobian_size 
    return [], [] 
 
 
def sysCall_init(): 
    global ikEnv 
    global ikGroup 
     
    bot = '.' 
    simBase=sim.getObject(bot) 
     
    simTip = sim.getObject(bot + '/tip') 
    simTarget = sim.getObject(bot + '/target') 
    simJoints=[] 
    for jointindex in range(1, 7):  # to exclude base as a joint 
        simJoints.append(sim.getObject("./link{}_resp/joint".format(jointindex + 
1))) 
    ikEnv=simIK.createEnvironment() 
    ikGroup=simIK.createIkGroup(ikEnv) 
24 
 
    
#simIK.setIkGroupCalculation(ikEnv,ikGroup,simIK.method_damped_least_squares,0.01,
10) 
    
simIK.addIkElementFromScene(ikEnv,ikGroup,simBase,simTip,simTarget,simIK.constrain
t_pose)