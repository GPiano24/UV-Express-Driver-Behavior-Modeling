import numpy as np
import pandas as pd
from queue import Queue
class Vehicle:
    def __init__(self, vehicleID, route, status, pickStops, dropStops, firstFlag, previousHiddenState, previousObservation):
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
        if self.Pickstops.empty() == False:
            return self.Pickstops.get()
        else :
            return "None"
    def getDropoff(self):
        if self.dropStops.empty() == False:
            return self.dropStops.get()
        else :
            return "None"
    def getPreviousHiddenState(self):
        return self.previousHiddenState
    def getPreviousObservation(self):
        return self.previousObservation