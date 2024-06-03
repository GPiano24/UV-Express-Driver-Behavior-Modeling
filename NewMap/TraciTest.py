import os, sys
if 'SUMO_HOME' in os.environ:
    sys.path.append(sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools')))
else:
    sys.exit("Environment variable 'SUMO_HOME' not defined")
import traci

sumoCmd = ["sumo-gui", "-c", "testMap.sumocfg", "-d", "200"]
traci.start(sumoCmd)

bus_stops = traci.busstop.getIDList()


for step in range(1000):

    if step == 10:
        traci.vehicle.add("UV_1", "Route_1", typeID="UV")
        traci.vehicle.setBusStop("UV_1", bus_stops[0], 10)
        print("Number of People in UV_1: ", traci.vehicle.getPersonNumber("UV_1"))

    if step == 100:
        traci.vehicle.add("UV_2", "Route_1", typeID="UV")
        traci.vehicle.setBusStop("UV_2", bus_stops[0], 10)

    traci.simulationStep()

traci.close()