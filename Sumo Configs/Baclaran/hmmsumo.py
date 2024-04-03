import re
import statistics
import numpy as np
import matplotlib.pyplot as plt
import itertools
import operator
from hmmlearn import hmm
from datetime import datetime
from pandas import DataFrame
from hmmlearn.hmm import GaussianHMM
from matplotlib import cm, pyplot as plt
import traci
import os
import sys
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

if 'SUMO_HOME' in os.environ:
    sys.path.append(sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools')))
else:
    sys.exit("Environment variable 'SUMO_HOME' not defined. Please set the 'SUMO_HOME' variable to the root directory of SUMO installation.")

sumo_binary = "sumo"  # Path to SUMO binary
sumo_cmd = [sumo_binary, "-c", os.path.abspath("Baclaran.sumocfg")]
traci.start(sumo_cmd)

sumo_actions = {
    'ChangeLaneLeft': {'change_lane': -1},  # Change lane to the left
    'ChangeLaneRight': {'change_lane': 1},  # Change lane to the right
    'Stop': {'stop': True},  # Stop
    'Go': {'accelerate': True},  # Accelerate
    'Load': {'load': True},  # Load
    'Unload': {'unload': True}  # Unload
}

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

passenger_states = {}

# Control SUMO simulation based on observed states and predicted actions
while traci.simulation.getMinExpectedNumber() > 0:
    # Advance simulation by one step
    traci.simulationStep()

    # Get the list of IDs for vehicles in the simulation
    vehicle_ids = traci.vehicle.getIDList()

    # Filter vehicles by type (e.g., only consider public vehicles)
    public_vehicle_ids = [veh_id for veh_id in vehicle_ids if traci.vehicle.getTypeID(veh_id) == "UV1"]

    # Loop through each public vehicle
    for vehicle_id in public_vehicle_ids:
        # Retrieve the observed state for the current vehicle
        observed_state = get_observed_state_from_sumo(vehicle_id)

        # If the observed state is not None, predict the next action
        if observed_state is not None:
            # Retrieve the current and previous hidden states
            current_hidden_state = observed_state
            previous_hidden_state = passenger_states.get(vehicle_id, None)  # Get the previous hidden state

            # Retrieve the previous observation
            previous_observation = None  # Set to None if no previous observation available
            if previous_hidden_state is not None:
                previous_observation = passenger_states.get(vehicle_id, None)  # Get the previous observation

            # Get the indices of the current and previous hidden states
            current_hidden_state_index = state_labels[current_hidden_state]
            previous_hidden_state_index = state_labels[previous_hidden_state] if previous_hidden_state is not None else None

            # Get the index of the previous observation
            previous_observation_index = observations.index(previous_observation) if previous_observation is not None else None

            # Use transition probabilities to predict the next hidden state
            if previous_hidden_state_index is not None:
                next_hidden_state_index = np.argmax(transition_probability[previous_hidden_state_index])
            else:
                # If no previous hidden state available, predict the next hidden state based on the current state
                next_hidden_state_index = np.argmax(transition_probability[current_hidden_state_index])

            # Use the emission probabilities of the next hidden state to predict the next observation
            emission_probabilities_next_state = emission_probability[next_hidden_state_index]

            # Select the next observation based on the emission probabilities of the next hidden state
            next_observation_index = np.random.choice(len(observations), p=emission_probabilities_next_state)
            predicted_next_observation = observations[next_observation_index]

            # Update passenger state
            passenger_states[vehicle_id] = current_hidden_state

            # Retrieve corresponding SUMO action
            next_action = sumo_actions[predicted_next_observation]

            # Control the current vehicle based on the predicted action
            if next_action.get('accelerate'):
                traci.vehicle.slowDown(vehicle_id, 0, 1)  # Accelerate
            elif next_action.get('change_lane'):
                traci.vehicle.changeLane(vehicle_id, next_action['change_lane'], 1)  # Change lane
            elif next_action.get('stop'):
                traci.vehicle.setSpeed(vehicle_id, 0)  # Stop
            elif next_action.get('load'):
                # Check if there are passengers waiting at the stop
                if traci.vehicle.getNextStops(vehicle_id):
                    # If there are passengers waiting, load them
                    passenger_states[vehicle_id] = "loaded"  # Update passenger state
                    traci.vehicle.setStop(vehicle_id, "stop_place", duration=0, laneIndex=0, pos=0, flags=1)  # Load passengers
            elif next_action.get('unload'):
                # Check if there are passengers on board
                if passenger_states.get(vehicle_id) == "loaded":
                    # If there are passengers on board, unload them
                    traci.vehicle.setStop(vehicle_id, "current_position", duration=0, laneIndex=0, pos=0, flags=0)  # Unload passengers
                    del passenger_states[vehicle_id]  # Update passenger state
            # Advance simulation by one step
            traci.simulationStep()

# Close connection to SUMO
traci.close()

