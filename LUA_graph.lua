function sysCall_init() 
 
    graph1=sim.getObject('/CartesianPoints') 
    graph2=sim.getObject('/JointAngles') 
    graph3=sim.getObject('/EulerAngles') 
     
    sensorPosX=sim.addGraphStream (graph1, 'x coord', '',0,{0,0,1})  
    sensorPosY=sim.addGraphStream (graph1, 'y coord','' ,0,{0,1,0})  
    sensorPosZ=sim.addGraphStream (graph1, 'z coord','' ,0,{0,1,1}) 
     
    simJoints = {} 
    for i=1,7,1 do 
        simJoints[i]=sim.getObject('./joint',{index=i-1}) 
    end 
     
    Angle1=sim.addGraphStream (graph2, 'joint[0]', '',0,{0.4,1,0.4}, math.pi)  
    Angle2=sim.addGraphStream (graph2, 'joint[1]','' ,0,{0.5,0.1,0.5}, math.pi)  
    Angle3=sim.addGraphStream (graph2, 'joint[2]','' ,0,{0.7,0,0.1}, math.pi) 
    Angle4=sim.addGraphStream (graph2, 'joint[3]', '',0,{1,0.5,0}, math.pi)  
    Angle5=sim.addGraphStream (graph2, 'joint[4]','' ,0,{1,1,0.1}, math.pi)  
    Angle6=sim.addGraphStream (graph2, 'joint[5]','' ,0,{0.7,0.6,0}, math.pi) 
    Angle7=sim.addGraphStream (graph2, 'joint[6]','' ,0,{0.6,0.3,0}, math.pi) 
     
    euler1= sim.addGraphStream (graph3, 'X', '',0,{1,0,0}, math.pi) 
    euler2= sim.addGraphStream (graph3, 'Y', '',0,{0,1,0}, math.pi) 
    euler3= sim.addGraphStream (graph3, 'Z', '',0,{0,0,1}, math.pi) 
 
 
end 
 
function sysCall_sensing() 
 
 
    sensor=sim.getObject( './connection') 
    sensorPos=sim.getObjectPosition (sensor,-1) 
    sim.setGraphStreamValue (graph1, sensorPosX, sensorPos[1])  
    sim.setGraphStreamValue (graph1, sensorPosY, sensorPos[2])  
    sim.setGraphStreamValue (graph1, sensorPosZ, sensorPos[3]) 
 
    sim.setGraphStreamValue (graph2, Angle1, sim.getJointPosition(simJoints[1]))  
    sim.setGraphStreamValue (graph2, Angle2, sim.getJointPosition(simJoints[2]))  
    sim.setGraphStreamValue (graph2, Angle3, sim.getJointPosition(simJoints[3])) 
    sim.setGraphStreamValue (graph2, Angle4, sim.getJointPosition(simJoints[4]))  
    sim.setGraphStreamValue (graph2, Angle5, sim.getJointPosition(simJoints[5]))  
    sim.setGraphStreamValue (graph2, Angle6, sim.getJointPosition(simJoints[6])) 
    sim.setGraphStreamValue (graph2, Angle7, sim.getJointPosition(simJoints[7]))  
     
23 
 
    --euler_connection = 
sim.getEulerAnglesFromMatrix(sim.poseToMatrix(sim.getObjectChildPose(simJoints[7])
)) 
    euler_connection = 
sim.getEulerAnglesFromMatrix(sim.getObjectMatrix(sensor,sim.getObject('.'))) 
     
    sim.setGraphStreamValue (graph3, euler1, euler_connection[1])  
    sim.setGraphStreamValue (graph3, euler2, euler_connection[2])  
    sim.setGraphStreamValue (graph3, euler3, euler_connection[3]) 
     
end