import re
import os, sys
from queue import Queue
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

class Vehicle:
    def __init__(self, vehicleID, status, pickStops, dropStops):
        self.vehicle = vehicleID
        self.status = status
        self.Pickstops = Queue()
        for stop in pickStops:
            self.Pickstops.put(stop)
        self.dropStops = Queue()
        for stop in dropStops:
            self.dropStops.put(stop)
    def getPickup(self):
        if self.Pickstops.empty() == False:
            return self.Pickstops.get()
    def getDropoff(self):
        if self.dropStops.empty() == False:
            return self.dropStops.get()


sorted_bus_stops = sorted(bus_stops, key=get_numeric_part)

PB_stops = sorted_bus_stops[:52]
BP_stops = sorted_bus_stops[52:]

PB_pickup = PB_stops[:45]
PB_dropoff = PB_stops[45:]


Vehicle_list = []
def addVehicle(veh_id, route_id, stops , typeID):
    traci.vehicle.add(veh_id, route_id, typeID=typeID)
    if route_id == "PB_route":
        PB_pickup = stops[:45]
        PB_dropoff = stops[45:]
        Vehicle_list.append(Vehicle(veh_id,"PickUp", PB_pickup, PB_dropoff))
    else:
        Vehicle_list.append(Vehicle(veh_id,"DropOff",[], stops))     

addVehicle("UV_0", "PB_route", PB_stops, "UV")


#traci.vehicle.add("UV_0","PB_route", typeID="UV")
#traci.vehicle.setBusStop("UV_0", PB_pickup[0], 10)

#traci.vehicle.add("UV_1","BP_route", typeID="UV")

for step in range(6000):

    for vehicle in Vehicle_list:
        vehicleID = vehicle.vehicle
        stops = traci.vehicle.getNextStops(vehicleID)
        Ids = [stop[2] for stop in stops]
        print ("Stops of Vehicle: ", vehicleID, Ids)

        #Change status to DropOff if UV has 16 passengers
        if traci.vehicle.getPersonNumber(vehicleID) == 16:
            vehicle.status = "DropOff"

        #add a new stop if UV is in PickUp mode
        if bool(Ids) == False and vehicle.status == "PickUp":
            stopID = vehicle.getPickup()
            traci.vehicle.setBusStop(vehicleID, stopID, 10)

        ## Add Drop Off Points
        elif bool(Ids) == False and vehicle.status == "DropOff":
            stopID = vehicle.getDropoff()
            traci.vehicle.setBusStop(vehicleID, stopID, 10)

    traci.simulationStep()

traci.close()