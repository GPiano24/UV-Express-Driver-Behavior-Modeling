import os, sys
if 'SUMO_HOME' in os.environ:
    sys.path.append(sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools')))
else:
    sys.exit("Environment variable 'SUMO_HOME' not defined")
import traci

sumoCmd = ["sumo-gui", "-c", "testMap.sumocfg", "-d", "200"]
traci.start(sumoCmd)

for step in range(1000):
    traci.simulationStep()

traci.close()