import os
import queue as Queue
import re
import sys
import random
import HMM as hmm
import sumolib
import traci
import traci.exceptions
if 'SUMO_HOME' in os.environ:
    sys.path.append(sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools')))
else:
    sys.exit("Environment variable 'SUMO_HOME' not defined")
from PedestrianEdges import PedestrianEdges
import Vehicle
import numpy as np
from Vehicle import Vehicle
from UVTraCIHelper import is_vehicle_in_front, get_observed_state_from_sumo, addVehicle, UVStep
from TraCIHelper import get_numeric_part, check_vehicle_exists, addRandomVehicle, addRandomPeople, addAgents

# Initialization of the model
states = ['Passenger', 'Vehicle', 'Stoplight']
state_labels = {state: i for i, state in enumerate(states)}
observations = ['ChangeLaneLeft', 'ChangeLaneRight', 'Stop', 'Go', 'Load', 'Unload']
file_name = 'data.csv'
modelClass = hmm.HMM(states, observations, file_name)
model_transition_probability = modelClass.get_model_transition_probabilities()
model_emission_probability = modelClass.get_model_emission_probabilities()

validation = False
validation_edges = [ "1054315838#0", "28740343", "352801326", "863419980#0", "111987075", "651079976", "109981573", "762672808"]

sumoCmd = ["sumo-gui", "-c", "UVExpressSimulation.sumocfg", "-d", "20"]
traci.start(sumoCmd)

# Constants
bus_stops = traci.busstop.getIDList()
sorted_bus_stops = sorted(bus_stops, key=get_numeric_part)

PB_stops = sorted_bus_stops[:52]
BP_stops = sorted_bus_stops[51:]

PB_pickup = PB_stops[:45]
PB_dropoff = PB_stops[45:]

BP_Pickup = BP_stops[:1]
BP_Dropoff = BP_stops[1:]

jeep_stops = sorted_bus_stops[:45] + sorted_bus_stops[52:]

Vehicle_list = []

pedestrian_edges = []
for stops in sorted_bus_stops:
    Lane = traci.busstop.getLaneID(stops)
    edge = traci.lane.getEdgeID(Lane)
    Stop = stops

    pedestrian_edges.append(PedestrianEdges(edge, Stop))

# Non-UV Agent Counts
n_cars = 150            # Number of car agents
n_motor = 200           # Number of motorcycle agents
n_buses = 50            # Number of bus agents
n_jeep = 20             # Number of jeep agents
n_people = 2000         # Number of pedestrian agents

addAgents(validation, n_cars, n_motor, n_buses, n_jeep, n_people, PB_stops, BP_stops, jeep_stops, pedestrian_edges, PB_pickup, PB_dropoff, BP_Pickup, BP_Dropoff)
    
checked_passengers = []
for step in range(6000):

    if not validation:
        if step%100 == 0:
            addVehicle(Vehicle_list, "PB" + str(step), "PB_route", PB_stops, BP_stops, "UV")
            addVehicle(Vehicle_list, "BP" + str(step+1), "BP_route", PB_stops, BP_stops, "UV")
    else:
        if step == 0:
           addVehicle(Vehicle_list, "PB" + str(step), "PB_route", PB_stops, BP_stops, "UV")
        if step == 50:
            addVehicle(Vehicle_list, "BP" + str(step+1), "BP_route", PB_stops, BP_stops, "UV")

    for vehicle in Vehicle_list:
        UVStep(vehicle, state_labels, model_transition_probability, model_emission_probability, observations, checked_passengers)
    
    traci.simulationStep()

traci.close()