import numpy as np
import pandas as pd
from queue import Queue
class Vehicle:
    def __init__(self, vehicleID, route, status, pickStops, dropStops, firstFlag, previousHiddenState, previousObservation):
        """
        The constructor for Vehicle class.
        Arguments:
            vehicleID {str} -- The identifier of the vehicle.
            route {str} -- The route of the vehicle.
            status {str} -- The status of the vehicle.
            pickStops {List} -- The list of pick up stops of the vehicle.
            dropStops {List} -- The list of drop off stops of the vehicle.
            firstFlag {bool} -- The flag to determine if the vehicle is the first vehicle.
            previousHiddenState {str} -- The previous hidden state of the vehicle.
            previousObservation {str} -- The previous observation of the vehicle.
        """
        self.vehicle = vehicleID
        self.route = route
        self.status = status
        self.firstFlag = firstFlag
        self.previousHiddenState = previousHiddenState
        self.previousObservation = previousObservation
        self.Pickstops = Queue()
        for stop in pickStops:
            self.Pickstops.put(stop)
        self.dropStops = Queue()
        for stop in dropStops:
            self.dropStops.put(stop)

    def getPickup(self):
        """
        Gets the pick up stops of the vehicle.

        Returns:
            pickStops {Queue} -- The list of pick up stops of the vehicle.
        """

        if self.Pickstops.empty() == False:
            return self.Pickstops.get()
        else :
            return "None"
        
    def getDropoff(self):
        """
        Gets the drop off stops of the vehicle.

        Returns:
            dropStops {Queue} -- The list of drop off stops of the vehicle.
        """

        if self.dropStops.empty() == False:
            return self.dropStops.get()
        else :
            return "None"
        
    def getPreviousHiddenState(self):
        """
        Gets the previous hidden state of the vehicle.

        Returns:
            previousHiddenState {str} -- The previous hidden state of the vehicle
        """
        return self.previousHiddenState
    
    def getPreviousObservation(self):
        """
        Gets the previous observation of the vehicle.

        Returns:
            previousObservation {str} -- The previous observation of the vehicle
        """
        return self.previousObservation