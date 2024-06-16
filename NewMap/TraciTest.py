import re
import os, sys
from queue import Queue
if 'SUMO_HOME' in os.environ:
    sys.path.append(sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools')))
else:
    sys.exit("Environment variable 'SUMO_HOME' not defined")
import traci
import numpy as np
import matplotlib.pyplot as plt
from hmmlearn import hmm
from matplotlib import cm, pyplot as plt
import traci
import os
import sys
import random
np.random.seed(1)

states = ['Passenger', 'Vehicle', 'Stoplight']
n_states = len(states)

# Oberservable states
observations = ['ChangeLaneLeft', 'ChangeLaneRight', 'Stop', 'Go', 'Load', 'Unload']
#						0					1		   2      3      4        5
n_observations = len(observations)

state_labels = {state: i for i, state in enumerate(states)}

# Load annotated events csv file
my_file = open('data.csv', 'r', encoding='utf-8-sig')

observed_states = []
observed_state_changes = []
observed_events = []

for line in my_file:
    l = [i.strip() for i in line.split(',')]
    observed_states.append(l[0]) 
    observed_state_changes.append(l[1])
    observed_events.append(l[2])

total_count = len(observed_states)

# Get state probabilities
sp_passenger = observed_states.count('Passenger') / total_count
sp_vehicle = observed_states.count('Vehicle') / total_count
sp_stoplight = observed_states.count('Stoplight') / total_count

state_probability = np.array([sp_passenger, sp_vehicle, sp_stoplight])

# Get transition states
temp = ''
transition_state = []
for cur_state in observed_state_changes:
    if temp == '':
        temp = cur_state
    else:
        if cur_state != 'N':
            word = temp+cur_state
            transition_state.append(word)
            temp = cur_state

# Get transition probabilities
total_p = transition_state.count('PP') + transition_state.count('PV') + transition_state.count('PS')
total_v = transition_state.count('VP') + transition_state.count('VV') + transition_state.count('VS')
total_s = transition_state.count('SP') + transition_state.count('SV') + transition_state.count('SS')

# P transition probabilities
tp_pp = transition_state.count('PP') / total_p
tp_pv = transition_state.count('PV') / total_p
tp_ps = transition_state.count('PS') / total_p

# V transition probabilities
tp_vp = transition_state.count('VP') / total_v
tp_vv = transition_state.count('VV') / total_v
tp_vs = transition_state.count('VS') / total_v

# S transition probabilities
tp_sp = transition_state.count('SP') / total_s
tp_sv = transition_state.count('SV') / total_s
tp_ss = transition_state.count('SS') / total_s

transition_probability = np.array([[tp_pp, tp_pv, tp_ps],
                                   [tp_vp, tp_vv, tp_vs],
                                   [tp_sp, tp_sv, tp_ss]])

# Get emission states
temp_events_numerical = []

for event in observed_events:
    if event == 'ChangeLaneLeft':
        temp_events_numerical.append(0)
    elif event == 'ChangeLaneRight':
        temp_events_numerical.append(1)
    elif event == 'Stop':
        temp_events_numerical.append(2)
    elif event == 'Go':
        temp_events_numerical.append(3)
    elif event == 'Load':
        temp_events_numerical.append(4)
    elif event == 'Unload':
        temp_events_numerical.append(5)

print(len(observed_states))
print(len(temp_events_numerical))
emission = []
for i in range(0, total_count):
    emission.append(observed_states[i]+str(temp_events_numerical[i]))   

events_numerical = np.array([temp_events_numerical]).reshape(-1,1)

# Get emission probabilities

# P to event X emission probabilities
total_ep = emission.count('Passenger0') + emission.count('Passenger1') + emission.count('Passenger2') + emission.count('Passenger3') + emission.count('Passenger4') + emission.count('Passenger5')
ep_p0 = emission.count('Passenger0') / total_ep
ep_p1 = emission.count('Passenger1') / total_ep
ep_p2 = emission.count('Passenger2') / total_ep
ep_p3 = emission.count('Passenger3') / total_ep
ep_p4 = emission.count('Passenger4') / total_ep
ep_p5 = emission.count('Passenger5') / total_ep

# V to event X emission probabilities
total_ev = emission.count('Vehicle0') + emission.count('Vehicle1') + emission.count('Vehicle2') + emission.count('Vehicle3') + emission.count('Vehicle4') + emission.count('Vehicle5')
ep_v0 = emission.count('Vehicle0') / total_ev
ep_v1 = emission.count('Vehicle1') / total_ev
ep_v2 = emission.count('Vehicle2') / total_ev
ep_v3 = emission.count('Vehicle3') / total_ev
ep_v4 = emission.count('Vehicle4') / total_ev
ep_v5 = emission.count('Vehicle5') / total_ev

# S to event X emission probabilities
total_es = emission.count('Stoplight0') + emission.count('Stoplight1') + emission.count('Stoplight2') + emission.count('Stoplight3') + emission.count('Stoplight4') + emission.count('Stoplight5')
ep_s0 = emission.count('Stoplight0') / total_es
ep_s1 = emission.count('Stoplight1') / total_es
ep_s2 = emission.count('Stoplight2') / total_es
ep_s3 = emission.count('Stoplight3') / total_es
ep_s4 = emission.count('Stoplight4') / total_es
ep_s5 = emission.count('Stoplight5') / total_es

emission_probability = np.array([[ep_p0, ep_p1, ep_p2, ep_p3, ep_p4, ep_p5],
                                 [ep_v0, ep_v1, ep_v2, ep_v3, ep_v4, ep_v5],
                                 [ep_s0, ep_s1, ep_s2, ep_s3, ep_s4, ep_s5]])

model = hmm.CategoricalHMM(n_components=len(states), n_features=len(observations), init_params="")

model.startprob_ = state_probability
model.transmat_ = transition_probability
model.emissionprob_ = emission_probability
model.fit(events_numerical)


log_probability, hidden_states = model.decode(events_numerical)
print("Log Probability: ", log_probability)
print("Hidden States: ")
for i in hidden_states[0:100]:
    print(states[i])
hidden_states = model.predict(events_numerical)
print("Hidden States: ")
for i in hidden_states[0:100]:
    print(states[i])

sumoCmd = ["sumo-gui", "-c", "testMap.sumocfg", "-d", "20"]
traci.start(sumoCmd)

bus_stops = traci.busstop.getIDList()

def get_numeric_part(bus_stop_id):
    match = re.search(r'(\d+)$', bus_stop_id)
    return int(match.group(1)) if match else float('inf')

def check_vehicle_exists(vehicleID):
    if vehicleID in traci.vehicle.getIDList():
        return True

class Vehicle:
    def __init__(self, vehicleID, route, status, pickStops, dropStops, firstFlag):
        self.vehicle = vehicleID
        self.route = route
        self.status = status
        self.firstFlag = firstFlag
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
BP_stops = sorted_bus_stops[51:]

PB_pickup = PB_stops[:45]
PB_dropoff = PB_stops[45:]

BP_Pickup = BP_stops[:1]
BP_Dropoff = BP_stops[1:]

Vehicle_list = []

def get_observed_state_from_sumo(vehicle_id):
    # Retrieve the vehicle's position
    vehicle_position = traci.vehicle.getPosition(vehicle_id)
    # Retrieve the vehicle's lane index
    lane_index = traci.vehicle.getLaneIndex(vehicle_id)
    
    # Check if there's a traffic light ahead
    if traci.vehicle.getNextTLS(vehicle_id) is not None:
        return 'Stoplight'

    # Check if there's a vehicle ahead
    leading_vehicle = traci.vehicle.getLeader(vehicle_id)
    if leading_vehicle is not None:
        # Retrieve the position of the leading vehicle
        leading_vehicle_position = traci.vehicle.getPosition(leading_vehicle)
        # If the distance between the vehicle and the leading vehicle is less than a threshold, consider it as detecting a vehicle
        if leading_vehicle_position[0] - vehicle_position[0] < 20:  # Adjust the threshold as needed
            return 'Vehicle'
    
    # Check if there's a pedestrian ahead (assuming pedestrians are represented as passengers)
    for veh_id in traci.vehicle.getIDList():
        if veh_id != vehicle_id:  # Ignore the current vehicle
            veh_position = traci.vehicle.getPosition(veh_id)
            if veh_position[0] == vehicle_position[0] and lane_index == traci.vehicle.getLaneIndex(veh_id):
                return 'Passenger'
    
    # If none of the conditions are met, return None
    return None

def addVehicle(veh_id, route_id, stops , typeID):
    traci.vehicle.add(veh_id, route_id, typeID=typeID)
    if route_id == "PB_route":
        PB_pickup = stops[:45]
        PB_dropoff = stops[45:]
        Vehicle_list.append(Vehicle(veh_id, route_id, "PickUp", PB_pickup, PB_dropoff, False))
        for stop in PB_dropoff:
            traci.vehicle.setBusStop(veh_id, stop, 10)
    elif route_id == "BP_route":
        BP_Pickup = BP_stops[:1]
        BP_Dropoff = BP_stops[1:]
        Vehicle_list.append(Vehicle(veh_id, route_id, "PickUp",BP_Pickup, BP_Dropoff, False))
        for stop in BP_Dropoff:
            traci.vehicle.setBusStop(veh_id, stop, 10)

def addRandomVehicle(vehID):
    options = ["Car", "Bus"]
    typeID = random.choice(options)
    routes = [f"r_{i}" for i in range(1, 51)]  # Create a list of routes r_1 to r_50
    route_id = random.choice(routes)  # Randomly select one route
    departTime = random.randint(0,5000)
    try:
        traci.vehicle.add(vehID, route_id, typeID=typeID, depart= departTime)
        print(f"Added vehicle v_{i}")
        print("departTime: ", departTime)
        print("Type: ", typeID)
    except traci.exceptions.TraCIException:
        print(f"Error adding vehicle {vehID} to route {route_id}")
        return

for i in range(70):
    addRandomVehicle(f"Random_{i}")

for step in range(6000):
    
    if step%100 == 0:
        addVehicle("PB" + str(len(Vehicle_list)), "PB_route", PB_stops, "UV")
        addVehicle("BP" + str(len(Vehicle_list)+1), "BP_route", BP_stops, "UV")

    for vehicle in Vehicle_list:
        vehicleID = vehicle.vehicle
        if check_vehicle_exists(vehicleID) == False:
            print("Vehicle Removed: ", vehicleID)
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
            elif vehicle.status == "MidTrip" and position.find("621030728") == 0 and vehicle.route == "PB_route":
                vehicle.status = "DropOff"
        else:
            if traci.vehicle.getPersonNumber(vehicleID) == 16 and vehicle.status == "PickUp":
                vehicle.status = "MidTrip"
            elif position.find("1054315838") == 0 and vehicle.status == "MidTrip":
                vehicle.status = "DropOff"

        #add a new stop if UV is in PickUp mode
        if vehicle.firstFlag == False and vehicle.status == "PickUp":
            vehicle.firstFlag = True
            stopID = vehicle.getPickup()
            if stopID != "None":
                traci.vehicle.setBusStop(vehicleID, stopID, 10)

        elif vehicle.status == "PickUp" and len(Ids) == len(PB_dropoff) or len(Ids) == len(BP_Dropoff):  
            stopID = vehicle.getPickup()
            if stopID != "None":
                print (stopID)
                personWaiting = traci.busstop.getPersonCount(stopID)
                print ("Stop ", stopID, " : ", personWaiting)
                if (personWaiting > 0):
                    traci.vehicle.setBusStop(vehicleID, stopID, 10)
            else:
                print("No more Pickups")
                vehicle.status = "MidTrip"

        ## Add Drop Off Points
        #elif bool(Ids) == False and vehicle.status == "DropOff":
        #    stopID = vehicle.getDropoff()
        #    if stopID != "None":
        #        traci.vehicle.setBusStop(vehicleID, stopID, 10)
        #    else:
        #        vehicle.status = "MidTrip"

        #Change UV Stats
        if vehicle.status == "PickUp":
            traci.vehicle.setMaxSpeed(vehicleID, 11.11)

        elif vehicle.status == "MidTrip":
            traci.vehicle.setMaxSpeed(vehicleID, 22.22)

        elif vehicle.status == "DropOff":
            traci.vehicle.setMaxSpeed(vehicleID, 11.11)

    traci.simulationStep()

traci.close()