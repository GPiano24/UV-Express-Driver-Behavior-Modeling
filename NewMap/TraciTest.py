import re
import os, sys
if 'SUMO_HOME' in os.environ:
    sys.path.append(sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools')))
else:
    sys.exit("Environment variable 'SUMO_HOME' not defined")
import traci

sumoCmd = ["sumo-gui", "-c", "testMap.sumocfg", "-d", "20"]
traci.start(sumoCmd)

bus_stops = traci.busstop.getIDList()

def get_numeric_part(bus_stop_id):
    match = re.search(r'(\d+)$', bus_stop_id)
    return int(match.group(1)) if match else float('inf')

sorted_bus_stops = sorted(bus_stops, key=get_numeric_part)

PB_stops = sorted_bus_stops[:52]
BP_stops = sorted_bus_stops[52:]

print("PB Stops: ", PB_stops)
print("BP Stops: ", BP_stops)

traci.vehicle.add("UV_0","PB_route", typeID="UV")
for stop in PB_stops:
    traci.vehicle.setBusStop("UV_0", stop, 10)

traci.vehicle.add("UV_1","BP_route", typeID="UV")
for stop in BP_stops:
    traci.vehicle.setBusStop("UV_1", stop, 10)

for step in range(6000):

    if step == 10:
        traci.vehicle.add("UV_2", "Route_1", typeID="UV")
        traci.vehicle.setBusStop("UV_2", bus_stops[0], 10)
        print("Number of People in UV_2: ", traci.vehicle.getPersonNumber("UV_1"))

    #if step == 100:
    #    traci.vehicle.add("UV_2", "Route_1", typeID="UV")
    #    traci.vehicle.setBusStop("UV_2", bus_stops[0], 10)

    traci.simulationStep()

traci.close()