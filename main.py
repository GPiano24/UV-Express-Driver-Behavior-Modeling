import numpy as np
from hmmlearn import hmm

# Hidden states
states = ['Passenger', 'Vehicle', 'Stoplight']
n_states = len(states)

# Oberservable states
observations = ['ChangeLaneLeft', 'ChangeLaneRight', 'Stop', 'Go', 'Load', 'Unload']
#						0					1		   2      3      4        5
n_observations = len(observations)

state_labels = {state: i for i, state in enumerate(states)}

# Integer labels for observable states
observation_labels = {observation: i for i, observation in enumerate(observations)}

# Initial state distribution (Change when data is available)
state_probability = np.array([0.75, 0.1375, 0.1125])

# State transition probabilities (Change when data is available)
transition_probability = np.array([[0.7823529412, 0.2, 0.01764705882],
								[0.107266436, 0.7993079585, 0.09342560554],
                                [0.09375, 0.375, 0.53125],])

# Observation probabilities (Change when data is avavilable)
emission_probability= np.array([[0, 0.1104651163, 0.2906976744, 0.2965116279, 0.1453488372, 0.1569767442],
								[0.4793103448, 0.4344827586, 0.04482758621, 0.03793103448, 0.00, 0.003448275862],
                                [0.015625, 0.046875, 0.46875, 0.46875, 0, 0],])



model = hmm.CategoricalHMM(n_components=n_states, n_features=n_observations)

model.startprob_ = state_probability
model.transmat_ = transition_probability
model.emissionprob_ = emission_probability

# Observation sequence (Change when data is avavilable)
observations_sequence = np.array([observation_labels[obs] for obs in ['Stop', 'Go', 'ChangeLaneLeft', 'ChangeLaneRight', 'Stop', 'Go', 'Stop', 'ChangeLaneLeft', 'ChangeLaneRight', 'ChangeLaneLeft', 'ChangeLaneRight', 'ChangeLaneLeft', 'ChangeLaneRight', 'ChangeLaneLeft', 'ChangeLaneRight', 'ChangeLaneLeft', 'ChangeLaneRight', 'ChangeLaneLeft', 'ChangeLaneRight', 'Go', 'Stop', 'Go', 'Stop', 'Go', 'Stop', 'Go', 'Stop', 'Go', 'Stop', 'Go', 'Stop', 'Go', 'Stop', 'ChangeLaneLeft', 'Unload', 'Go', 'Stop', 'ChangeLaneLeft', 'ChangeLaneRight', 'Stop', 'Go', 'Stop', 'Stop', 'ChangeLaneLeft', 'Unload', 'Go', 'Stop', 'Stop', 'Go', 'Stop', 'Stop', 'Go', 'Stop', 'Stop', 'Go', 'Go', 'Stop', 'Stop', 'ChangeLaneLeft', 'ChangeLaneRight', 'Stop', 'Stop', 'ChangeLaneLeft', 'ChangeLaneRight', 'Go', 'Stop', 'Go', 'Stop', 'Go', 'ChangeLaneLeft', 'ChangeLaneRight', 'Stop', 'Stop', 'Stop', 'Stop', 'Go', 'Stop', 'Go', 'Go', 'Go', 'ChangeLaneLeft', 'Unload']]).reshape(-1, 1)
observations_sequence

# Predict

log_probability, hidden_states = model.decode(observations_sequence)
hidden_states = model.predict(observations_sequence)

print("Most likely hidden states:", hidden_states)
