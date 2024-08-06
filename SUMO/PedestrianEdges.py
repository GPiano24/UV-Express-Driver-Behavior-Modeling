class PedestrianEdges:
    """
    A class to represent pedestrian edges and associated bus stops in a transportation network.

    Attributes:
        edge {str} -- The identifier or description of the pedestrian edge.
        busStop {str} -- The identifier or description of the bus stop associated with the pedestrian edge.
    """
    def __init__(self, edge, busStop):
        """
        The constructor for PedestrianEdges class.
        Arguments:
            edge {str} -- The identifier or description of the pedestrian edge.
            busStop {str} -- The identifier or description of the bus stop associated with the pedestrian edge.
        """

        self.edge = edge
        self.busStop = busStop

    def getEdge(self):
        """
        Gets the pedestrian edge.
        
        Returns:
            edge {str} -- The identifier or description of the pedestrian edge.
        """
        return self.edge
    
    def getBusStop(self):
        """
        Gets the bus stop associated with the pedestrian edge.
        
        Returns:
            busStop{str} -- The identifier or description of the bus stop associated with the pedestrian edge.
        """
        return self.busStop