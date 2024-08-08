import numpy as np
from hmmlearn import hmm
np.random.seed(1)

class HMM(object):
    def __init__(self, states, observations, file_name):
        """Class constructor for Hidden Markov Model
        Arguments:
            states {List} -- list of states
            observations {List} -- list of observations
            file_name {str} -- file name of the annotated data
        """
        self.states = states
        self.n_states = len(states)
        self.observations = observations
        self.n_observations = len(observations)
        self.file_name = file_name
        self.model = self.create_model()

    def create_model(self):
        """Creates the model for the Hidden Markov Model
        Returns:
            model -- Hidden Markov Model
        """
        observed_states, observed_state_changes, observed_events = self.load_annotated_data(self.file_name)
        start_probabilities = self.calculate_start_probabilities(observed_states)
        transition_states = self.get_transition_states(observed_state_changes)
        transition_probabilities = self.calculate_transition_probabilities(transition_states)
        emission, events_numerical = self.get_emission_states(observed_states, observed_events, len(observed_states))
        emission_probabilities = self.calculate_emission_probabilities(emission)
        model = self.train_model(start_probabilities, transition_probabilities, emission_probabilities, events_numerical)
        return model

    def load_annotated_data(self, file_name):
        """Loads the annotated data from the file
        Arguments:
            file_path {str} -- path to the file
        Returns:
            observed_states {List} -- list of observed states
            observed_state_changes {List} -- list of observed state changes
            observed_events {List} -- list of observed events
        """
        my_file = open(file_name, 'r', encoding='utf-8-sig')

        # Get the data from the file
        observed_states = []
        observed_state_changes = []
        observed_events = []

        for line in my_file:
            l = [i.strip() for i in line.split(',')]
            observed_states.append(l[0]) 
            observed_state_changes.append(l[1])
            observed_events.append(l[2])
        
        return observed_states, observed_state_changes, observed_events
    
    def calculate_start_probabilities(self, observed_states):
        """Calculates the start probabilities
        Arguments:
            observed_states {List} -- list of observed states
        Returns:
            start_probabilities {List} -- start probabilities
        """
        total_count = len(observed_states)
        start_probabilities = np.zeros(self.n_states)
        for state in self.states:
            start_probabilities[self.states.index(state)] = observed_states.count(state) / total_count
        return start_probabilities
    
    def get_transition_states(self, observed_state_changes):
        """Gets the transition states
        Arguments:
            observed_state_changes {List} -- list of observed state changes
        Returns:
            transition_states {List} -- list of transition states
        """
        previous_state = ''
        transition_states = []
        for current_state in observed_state_changes:
            if previous_state == '':
                previous_state = current_state
            else:
                transition_state = previous_state + current_state
                transition_states.append(transition_state)
                previous_state = current_state
        return transition_states
    
    def calculate_transition_probabilities(self, transition_states):
        """Calculates the transition probabilities
        Arguments:
            transition_states {List} -- list of transition states
        Returns:
            transition_probabilities {List} -- transition probabilities
        """
        totals = []
        for state in self.states:
            total = sum (1 for transition_state in transition_states if transition_state.startswith(state[0]))
            totals.append(total)

        transition_probabilities = np.zeros((self.n_states, self.n_states))
        for state0 in self.states:
            for state1 in self.states:
                transition_probabilities[self.states.index(state0)][self.states.index(state1)] = sum(1 for transition_state in transition_states if transition_state.startswith(state0[0] + state1[0])) / totals[self.states.index(state0)]

        return transition_probabilities
    
    def get_emission_states(self, observed_states, observed_events, n_observed_states):
        """Gets the emission states
        Arguments:
            observed_states {List} -- list of possible observed states
            observed_events {List} -- list of recorded observed events
            n_states {int} -- number of states
        Returns:
            emission {List} -- list of emission states
            events_numerical {List} -- list of numerical events
        """
        temp_events_numerical = []
        for event in observed_events:
            temp_events_numerical.append(self.observations.index(event))
        events_numerical = np.array([temp_events_numerical]).reshape(-1, 1)

        emission = []
        for i in range(0, n_observed_states):
            emission.append(observed_states[i] + str(temp_events_numerical[i]))
        
        return emission, events_numerical
    
    def calculate_emission_probabilities(self, emission):
        """Calculates the emission probabilities
        Arguments:
            emission {List} -- list of emission states
        Returns:
            emission_probabilities {List} -- emission probabilities
        """
        emission_probabilities = np.zeros((self.n_states, self.n_observations))
        for state in self.states:
            total = sum(1 for e in emission if e.startswith(state))
            for i in range(0,self.n_observations):
                emission_probabilities[self.states.index(state)][i] = sum(1 for e in emission if e.startswith(state + str(i)))/total
        return emission_probabilities
    
    def train_model(self, start_probabilities, transition_probabilities, emission_probabilities, events_numerical):
        """Trains the model
        Arguments:
            start_probabilities {List} -- start probabilities
            transition_probabilities {List} -- transition probabilities
            emission_probabilities {List} -- emission probabilities
            events_numerical {List} -- list of numerical events
        Returns:
            model -- trained model
        """
        model = hmm.CategoricalHMM(n_components=self.n_states, n_features=self.n_observations)

        model.startprob_ = start_probabilities
        model.transmat_ = transition_probabilities
        model.emissionprob_ = emission_probabilities
        model.fit(events_numerical)
        return model
    
    def get_model(self):
        """Gets the Hidden Markov model
        Returns:
            model -- model
        """
        return self.model
    
    def get_model_transition_probabilities(self):
        """Gets the transition probabilities of the model
        Returns:
            transition_probabilities {List} -- transition probabilities
        """
        return self.model.transmat_
    
    def get_model_emission_probabilities(self):
        """Gets the emission probabilities of the model
        Returns:
            emission_probabilities {List} -- emission probabilities
        """
        return self.model.emissionprob_