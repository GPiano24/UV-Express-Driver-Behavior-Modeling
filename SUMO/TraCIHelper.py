import traci
import sumolib
import re
import random


def get_numeric_part(bus_stop_id):
    """
    Gets the numeric part of the bus stop ID

    Arguments:
        bus_stop_id {str} -- The bus stop ID

    Returns:
        int -- The numeric part of the bus stop ID
    """

    match = re.search(r'(\d+)$', bus_stop_id)
    return int(match.group(1)) if match else float('inf')

def check_vehicle_exists(vehicleID):
    """
    Checks if a vehicle exists in the simulation

    Arguments:
        vehicleID {str} -- The vehicle ID
    """

    if vehicleID in traci.vehicle.getIDList():
        return True
    return False

#Vehicles Other than UVs
def addRandomVehicle(type, vehID, vehID_num,PB_stops, BP_stops, jeep_stops):
    """
    Adds a random vehicle to the simulation

    Arguments:
        type {str} -- The type of vehicle
        vehID {str} -- The vehicle ID
        vehID_num {int} -- The vehicle ID number
        PB_stops {List} -- List of bus stops for the PB route
        BP_stops {List} -- List of bus stops for the BP route
        jeep_stops {List} -- List of bus stops for the jeep route
    """
    typeID = type
    routes = [f"r_{i}" for i in range(1, 31)]  # Create a list of routes r_1 to r_50
    if typeID == "Car":
        route_id = random.choice(routes)  # Randomly select one route
        vehID = vehID.replace("Random", "Car")
    elif typeID == "Motor":
        route_id = random.choice(routes)
        vehID = vehID.replace("Random", "Motor")
    elif typeID == "Jeep":
        route_id = "jeep_route"
        vehID = vehID.replace("Random", "Jeep")
        stops = jeep_stops
    elif typeID == "Bus":
        vehID = vehID.replace("Random", "Bus")
        choices = ["PB_route", "BP_route"]
        route_id = random.choice(choices)
        if route_id == "PB_route":
            stops = PB_stops
        else:
            stops = BP_stops
    departTime = random.randint(0,5000)
    try:
        traci.vehicle.add(vehID, route_id, typeID=typeID, depart= departTime)
        print(f"Added vehicle v_{vehID_num}")
        print("departTime: ", departTime)
        print("Type: ", typeID)
        if typeID == "Bus" or typeID == "Jeep":
           for stop in stops:
                traci.vehicle.setBusStop(vehID, stop, 10)
    except traci.exceptions.TraCIException:
        print(f"Error adding vehicle {vehID} to route {route_id}")
        return

#Add Random People
def addRandomPeople(p_id, edgelist, PB_pickup, PB_dropoff, BP_Pickup, BP_Dropoff, jeep_stops):
    """
    Adds a random person to the simulation

    Arguments:
        p_id {str} -- The person ID
        edgelist {List} -- List of pedestrian edges
        PB_pickup {List} -- List of bus stops for the PB route
        PB_dropoff {List} -- List of bus stops for the PB route
        BP_Pickup {List} -- List of bus stops for the BP route
        BP_Dropoff {List} -- List of bus stops for the BP route
        jeep_stops {List} -- List of bus stops for the jeep route
    """

    options = ["UV", "Walk", "Bus", "Jeep"]
    p_action = random.choice(options)
    edges = []
    for edge in edgelist:
        edges.append(edge.getEdge())

    if p_action == "Walk":
        p_id = p_id.replace("Person", "Walking")
        start = random.choice(edges)
        destination = random.choice(edges)
        edge_length = traci.lane.getLength(f"{start}_0")
        position = random.uniform(0, edge_length - 1)
        endposition = random.uniform(0, edge_length - 1)
        departTime = random.randint(0,5000)
        try:
            traci.person.add(p_id, start,pos=position, depart= departTime)
            traci.person.appendWalkingStage(p_id, start, endposition)
            print("Added random walking person")
            traci.person.setColor(p_id, (255, 0, 0, 255))
        except traci.exceptions.TraCIException:
            print(f"Error adding person {p_id} to edge {start}")

    elif p_action == "UV":
        p_id = p_id.replace("Person", "UVRider")
        start = random.choice(edges)
        edge_length = traci.lane.getLength(f"{start}_0")
        position = random.uniform(0, edge_length - 1)
        near_stops = []
        for edge in edgelist:
            if edge.getEdge() == start:
                near_stops.append(edge.getBusStop())
        stop = random.choice(near_stops)
        departTime = random.randint(0,5000)
        flag = "Valid"
        Lines = ""
        if stop in PB_pickup:
            destination = random.choice(PB_dropoff)
            dest_edge = traci.lane.getEdgeID(traci.busstop.getLaneID(destination))
            print (f"Start: {start}, Stop: {stop}, Destination: {destination}")
        elif stop in BP_Pickup:
            destination = random.choice(BP_Dropoff)
            dest_edge = traci.lane.getEdgeID(traci.busstop.getLaneID(destination))
            print (f"Start: {start}, Stop: {stop}, Destination: {destination}")
        else :
            flag = "Invalid"
        if (flag == "Valid"):
            try:
                traci.person.add(p_id, start,position, depart= departTime)
                traci.person.appendWalkingStage(p_id, start, 0, stopID = stop)
                traci.person.appendDrivingStage(p_id, dest_edge, "UV",stopID= destination)
                print("Added random person to UV")
                traci.person.setColor(p_id, (0, 0, 255, 255))
            except traci.exceptions.TraCIException:
                print(f"Error adding person {p_id} to edge {start} for UV")
    elif p_action == "Bus":
        p_id = p_id.replace("Person", "BusRider")
        start = random.choice(edges)
        edge_length = traci.lane.getLength(f"{start}_0")
        position = random.uniform(0, edge_length - 1)
        near_stops = []
        for edge in edgelist:
            if edge.getEdge() == start:
                near_stops.append(edge.getBusStop())
        stop = random.choice(near_stops)
        departTime = random.randint(0,5000)
        flag = "Valid"
        if stop in PB_pickup:
            destination = random.choice(PB_dropoff)
            dest_edge = traci.lane.getEdgeID(traci.busstop.getLaneID(destination))
            print (f"Start: {start}, Stop: {stop}, Destination: {destination}")
        elif stop in BP_Pickup:
            destination = random.choice(BP_Dropoff)
            dest_edge = traci.lane.getEdgeID(traci.busstop.getLaneID(destination))
            print (f"Start: {start}, Stop: {stop}, Destination: {destination}")
        else :
            flag = "Invalid"
        if (flag == "Valid"):
            try:
                traci.person.add(p_id, start,position, depart= departTime)
                traci.person.appendWalkingStage(p_id, start, 0, stopID = stop)
                traci.person.appendDrivingStage(p_id, dest_edge, "Bus",stopID= destination)
                print("Added random person to Bus")
                traci.person.setColor(p_id, (0, 255, 0, 255))
            except traci.exceptions.TraCIException:
                print(f"Error adding person {p_id} to edge {start} for Bus")
    elif p_action == "Jeep":
        p_id = p_id.replace("Person", "JeepRider")
        start = random.choice(edges)
        edge_length = traci.lane.getLength(f"{start}_0")
        position = random.uniform(0, edge_length - 1)
        near_stops = []
        for edge in edgelist:
            if edge.getEdge() == start:
                near_stops.append(edge.getBusStop())
        stop = random.choice(near_stops)
        departTime = random.randint(0,5000)
        flag = "Valid"
        eligible_stops = []
        for stops in jeep_stops:
            if get_numeric_part(stop) < 45:
                if get_numeric_part(stops) > get_numeric_part(stop):
                    eligible_stops.append(stops)
            elif get_numeric_part(stop) > 44:
                if get_numeric_part(stops) > get_numeric_part(stop):
                    eligible_stops.append(stops)
        if (eligible_stops == []):
            flag = "Invalid"
        else:
            destination = random.choice(eligible_stops)
            dest_edge = traci.lane.getEdgeID(traci.busstop.getLaneID(destination))
            print (f"Start: {start}, Stop: {stop}, Destination: {destination}")
        if (flag == "Valid"):
            try:
                traci.person.add(p_id, start,position, depart= departTime)
                traci.person.appendWalkingStage(p_id, start, 0, stopID = stop)
                traci.person.appendDrivingStage(p_id, dest_edge, "Jeep",stopID= destination)
                print("Added random person to Jeep")
                traci.person.setColor(p_id, (255, 0, 255, 255))
            except traci.exceptions.TraCIException:
                print(f"Error adding person {p_id} to edge {start} for Jeep")

def addAgents(validation, n_cars, n_motor, n_jeep, n_bus, n_people, PB_stops, BP_stops, jeep_stops, pedestrian_edges, PB_pickup, PB_dropoff, BP_Pickup, BP_Dropoff):
    """
    Adds multiple random vehicles and people to the simulation
    
    Arguments:
        validation {bool} -- If True, adds only one vehicle and one person for validation
        n_cars {int} -- Number of cars to add
        n_motor {int} -- Number of motorcycles to add
        n_jeep {int} -- Number of jeeps to add
        n_bus {int} -- Number of buses to add
        n_people {int} -- Number of people to add
        PB_stops {List} -- List of bus stops for the PB route
        BP_stops {List} -- List of bus stops for the BP route
        jeep_stops {List} -- List of bus stops for the jeep route
        pedestrian_edges {List} -- List of pedestrian edges
        PB_pickup {List} -- List of bus stops for the PB route
        PB_dropoff {List} -- List of bus stops for the PB route
        BP_Pickup {List} -- List of bus stops for the BP route
        BP_Dropoff {List} -- List of bus stops for the BP route
    """
    if not validation:
        for i in range(n_cars):
            addRandomVehicle("Car", f"Random_{i}", i, PB_stops, BP_stops, jeep_stops)
        for i in range(n_motor):
            addRandomVehicle("Motor", f"Random_{i}", i, PB_stops, BP_stops, jeep_stops)
        for i in range(n_jeep):
            addRandomVehicle("Jeep", f"Random_{i}", i, PB_stops, BP_stops, jeep_stops)
        for i in range(n_bus):
            addRandomVehicle("Bus", f"Random_{i}", i, PB_stops, BP_stops, jeep_stops)

        for i in range (n_people):
            addRandomPeople(f"Person_{i}", pedestrian_edges, PB_pickup, PB_dropoff, BP_Pickup, BP_Dropoff, jeep_stops)