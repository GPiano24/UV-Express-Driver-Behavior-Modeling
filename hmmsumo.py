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

model = hmm.CategoricalHMM(n_components=len(states), n_features=len(observations))

model.startprob_ = state_probability
model.transmat_ = transition_probability
model.emissionprob_ = emission_probability

log_probability, hidden_states = model.decode(events_numerical)
hidden_states = model.predict(events_numerical)