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

def check_vehicle_exists(vehicleID):
    return vehicleID in traci.vehicle.getIDList()

class Vehicle:
    def __init__(self, vehicleID, route, status, pickStops, dropStops):
        self.vehicle = vehicleID
        self.route = route
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
        else :
            return "None"
    def getDropoff(self):
        if self.dropStops.empty() == False:
            return self.dropStops.get()
        else :
            return "None"


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
        Vehicle_list.append(Vehicle(veh_id, route_id, "PickUp", PB_pickup, PB_dropoff))
    else:
        Vehicle_list.append(Vehicle(veh_id, route_id, "MidTrip",[], stops))     

addVehicle("UV_0", "PB_route", PB_stops, "UV")


for step in range(6000):

    for vehicle in Vehicle_list:
        vehicleID = vehicle.vehicle
        if check_vehicle_exists(vehicleID) == False:
            Vehicle_list.remove(vehicle)
            continue
        stops = traci.vehicle.getNextStops(vehicleID)
        Ids = [stop[2] for stop in stops]
        position = traci.vehicle.getRoadID(vehicleID)

        #Change status Of UV
        if vehicle.route == "PB_route":
            if traci.vehicle.getPersonNumber(vehicleID) == 16 and vehicle.status == "PickUp":
                vehicle.status = "MidTrip"
            elif vehicle.status == "PickUp" and position == "27498964" and vehicle.route == "PB_route":
                vehicle.status = "MidTrip"
            elif vehicle.status == "MidTrip" and position.find("621030728") and vehicle.route == "PB_route":
                vehicle.status = "DropOff"
        else:
            if position == "27498964" and vehicle.status == "MidTrip":
                vehicle.status = "DropOff"

        #add a new stop if UV is in PickUp mode
        if bool(Ids) == False and vehicle.status == "PickUp":
            stopID = vehicle.getPickup()
            if stopID != "None":
                traci.vehicle.setBusStop(vehicleID, stopID, 10)
            else:
                vehicle.status = "MidTrip"

        ## Add Drop Off Points
        elif bool(Ids) == False and vehicle.status == "DropOff":
            stopID = vehicle.getDropoff()
            if stopID != "None":
                traci.vehicle.setBusStop(vehicleID, stopID, 10)
            else:
                vehicle.status = "MidTrip"

        #Change UV Stats
        if vehicle.status == "PickUp":
            traci.vehicle.setMaxSpeed(vehicleID, 11.11)

        elif vehicle.status == "MidTrip":
            traci.vehicle.setMaxSpeed(vehicleID, 22.22)

        elif vehicle.status == "DropOff":
            traci.vehicle.setMaxSpeed(vehicleID, 11.11)

    traci.simulationStep()

traci.close()