import traci
import sumolib
import Vehicle
import numpy as np

def is_vehicle_in_front(vehicleID, leading_vehicle, distance_threshold=10):
    # Get current lane ID and lane position of the vehicle
    if leading_vehicle is not None:
        current_lane_id = traci.vehicle.getLaneID(vehicleID)
        current_lane_position = traci.vehicle.getLanePosition(vehicleID)
        
        # Get list of all vehicles known to TraCI
        nearby_vehicles = traci.vehicle.getIDList()
                
        lead_id, distance = leading_vehicle
        if distance <= distance_threshold:
            return True
        return False
    return False

def get_observed_state_from_sumo(vehicle_id):
    # Retrieve the vehicle's position
    vehicle_position = traci.vehicle.getPosition(vehicle_id)
    # Retrieve the vehicle's lane index
    lane_index = traci.vehicle.getLaneIndex(vehicle_id)
    
    # Check if there's a pedestrian ahead (assuming pedestrians are represented as passengers)
    for person_id in traci.person.getIDList():
        person_position = traci.person.getPosition(person_id)
        is_full = len(traci.vehicle.getPersonIDList(vehicle_id)) >= 16
        if not is_full and "waiting for " in (traci.person.getStage(person_id)).description and sumolib.geomhelper.distance(traci.vehicle.getPosition(vehicle_id), person_position) <= 20:
            return 'Passenger'

    # Detect if a passenger on board is ready to alight
    passengers_on_board = traci.vehicle.getPersonIDList(vehicle_id)
    for passenger_id in passengers_on_board:
        edges = traci.person.getEdges(passenger_id, traci.person.getRemainingStages(passenger_id) - 1)
        if edges:
            passenger_destination_edge_id = edges[0]
            try:
                passenger_destination_length = traci.lane.getLength(passenger_destination_edge_id)
                passenger_destination_pos = traci.simulation.convert2D(passenger_destination_edge_id, passenger_destination_length)
                if sumolib.geomhelper.distance(traci.vehicle.getPosition(vehicle_id), passenger_destination_pos) <= 10:
                    return 'Passenger'
            except traci.exceptions.TraCIException:
                None
            
    # Check if there's a traffic light ahead
    if traci.vehicle.getNextTLS(vehicle_id) is not None:
        return 'Stoplight'

    # Check if there's a vehicle ahead
    leading_vehicle = traci.vehicle.getLeader(vehicle_id, 10)
    if is_vehicle_in_front(vehicle_id, leading_vehicle):
        return 'Vehicle'
    
    # If none of the conditions are met, return None
    return None

def addVehicle(Vehicle_list, veh_id, route_id, PB_stops, BP_stops, typeID):
    traci.vehicle.add(veh_id, route_id, typeID=typeID, line="UV")
    if route_id == "PB_route":
        PB_pickup = PB_stops[:45]
        PB_dropoff = PB_stops[45:]
        Vehicle_list.append(Vehicle.Vehicle(veh_id, route_id, "PickUp", PB_pickup, PB_dropoff, False, None, None))
        for stop in PB_dropoff:
            traci.vehicle.setBusStop(veh_id, stop, 10)
    elif route_id == "BP_route":
        BP_Pickup = BP_stops[:1]
        BP_Dropoff = BP_stops[1:]
        Vehicle_list.append(Vehicle.Vehicle(veh_id, route_id, "PickUp",BP_Pickup, BP_Dropoff, False, None, None))
        for stop in BP_Dropoff:
            traci.vehicle.setBusStop(veh_id, stop, 10)

def UVStep(vehicle, state_labels, model_transition_probability, model_emission_probability, observations, checked_passengers):
    vehicleID = vehicle.vehicle
    position = traci.vehicle.getRoadID(vehicleID)
    #if validation:
            #if position in validation_edges:
                #if previous != position:
                    #print("Vehicle ", vehicleID, " is at ", position, "at step ", step)

    observed_state = get_observed_state_from_sumo(vehicleID)

    next_action = None

    if observed_state is not None:
        current_hidden_state = observed_state
        previous_hidden_state = vehicle.getPreviousHiddenState()

        previous_observation = None
        if previous_hidden_state is not None:
            previous_observation = vehicle.getPreviousObservation()

        current_hidden_state_index = state_labels[current_hidden_state]
        previous_hidden_state_index = state_labels[previous_hidden_state] if previous_hidden_state is not None else None

        previous_observation_index = observations.index(previous_observation) if previous_observation is not None else None

        if previous_hidden_state_index is not None and previous_observation_index is not None:
            next_hidden_state = np.argmax(model_transition_probability[previous_hidden_state_index])
        else:
            next_hidden_state = np.argmax(model_transition_probability[current_hidden_state_index])

        emission_probabilities_next_state = model_emission_probability[next_hidden_state]

        invalid_obs = True
        while invalid_obs:
            next_observation_index = np.random.choice(len(observations), p=emission_probabilities_next_state)
            predicted_next_observation = observations[next_observation_index]
            if current_hidden_state == 'Vehicle' and predicted_next_observation in ['ChangeLaneLeft', 'ChangeLaneRight']:
                # Check if the vehicle is already at the edge of the lane network
                if traci.vehicle.getLaneIndex(vehicleID) == 0 and predicted_next_observation == 'ChangeLaneLeft':
                    continue  # Skip this prediction, it's invalid
                elif traci.vehicle.getLaneIndex(vehicleID) == traci.vehicle.getLaneNumber(vehicleID) - 1 and predicted_next_observation == 'ChangeLaneRight':
                    continue  # Skip this prediction, it's invalid
                else:
                    invalid_obs = False
            else:
                invalid_obs = False

        vehicle.previousHiddenState = current_hidden_state
        vehicle.previousObservation = predicted_next_observation
        next_action = predicted_next_observation
            
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
        elif vehicle.status == "PickUp" and position == "649171196" and vehicle.route == "BP_route":
            vehicle.status = "MidTrip"
        elif position.find("1054315838#0") == 0 and vehicle.status == "MidTrip":
            vehicle.status = "DropOff"

    if observed_state == 'Passenger':
        traci.vehicle.setSpeed(vehicleID, 0)
        stopped = False
        # Check if there are passengers within 10 meters to pick up
        if len(traci.vehicle.getPersonIDList(vehicleID)) < 16:
            passengers_nearby = traci.person.getIDList()
            to_pickup_count = 0
            for passenger_id in passengers_nearby:
                is_waiting = "waiting for " in (traci.person.getStage(passenger_id)).description
                passenger_position = traci.person.getPosition(passenger_id)
                is_full = len(traci.vehicle.getPersonIDList(vehicleID)) >= 16
                if not is_full and is_waiting and sumolib.geomhelper.distance(traci.vehicle.getPosition(vehicleID), passenger_position) <= 20 and passenger_id not in checked_passengers:
                    to_pickup_count += 1
                    checked_passengers.append(passenger_id)
            if to_pickup_count != 0:
                try:
                    traci.vehicle.setStop(vehicleID, traci.vehicle.getRoadID(vehicleID), traci.vehicle.getLanePosition(vehicleID) + 10.0, 0, duration=(10*to_pickup_count))
                except:
                    try:
                        traci.vehicle.setStop(vehicleID, traci.vehicle.getRoadID(vehicleID), traci.vehicle.getLanePosition(vehicleID) + 10.0, 1, duration=(10*to_pickup_count))
                    except:
                        None
                            
                        
        passengers_on_board = traci.vehicle.getPersonIDList(vehicleID)
        for passenger_id in passengers_on_board:
            current_stage = traci.person.getStage(passenger_id)
            
            if current_stage and "driving" in current_stage.description:
                edges = traci.person.getEdges(passenger_id, traci.person.getRemainingStages(passenger_id) - 1)
                if edges:
                    passenger_destination_edge_id = edges[0]  # Assuming the last edge is the first in the list
                    
                    try:
                        num_lanes = traci.edge.getLaneNumber(passenger_destination_edge_id)
                    except traci.exceptions.TraCIException as e:
                        print(f"Failed to get number of lanes: {e}")
                        continue
                        
                    passenger_destination_lane_id = f"{passenger_destination_edge_id}_0"
                        
                    try:
                        passenger_destination_length = traci.lane.getLength(passenger_destination_lane_id)
                    except traci.exceptions.TraCIException as e:
                        print(f"Failed to get lane length: {e}")
                        continue
                        
                    passenger_destination_pos = traci.simulation.convert2D(passenger_destination_edge_id, passenger_destination_length)
                        
                    # Calculate distance between vehicle and drop-off point
                    vehicle_position = traci.vehicle.getPosition(vehicleID)
                    distance_to_destination = sumolib.geomhelper.distance(vehicle_position, passenger_destination_pos)
                        
                    # Check if vehicle is close enough to the drop-off point
                    if distance_to_destination <= 10:                            
                        # Set a stop near the drop-off point
                        try:
                            traci.vehicle.setStop(vehicleID, traci.vehicle.getRoadID(vehicleID), traci.vehicle.getLanePosition(vehicleID), 0, duration=10)
                        except traci.exceptions.TraCIException as e:
                            print(f"Failed to set stop: {e}")
                            continue
                            
                        try:
                            traci.person.appendWalkingStage(passenger_id, [passenger_destination_edge_id], arrivalPos=passenger_destination_length)

                            traci.vehicle.moveToXY(vehicleID, passenger_destination_edge_id, 0, passenger_destination_pos[0], passenger_destination_pos[1])
                        except traci.exceptions.TraCIException as e:
                            print(f"Failed to perform drop-off actions: {e}")
                            continue
        if vehicle.status == "MidTrip":
            traci.vehicle.setMaxSpeed(vehicleID, 22.22)
        else:
            traci.vehicle.setMaxSpeed(vehicleID, 11.11)

    if observed_state == 'Vehicle':
        if next_action == 'ChangeLaneLeft':
            traci.vehicle.changeLane(vehicleID, traci.vehicle.getLaneIndex(vehicleID) - 1, 500)
        elif next_action == 'ChangeLaneRight':
            traci.vehicle.changeLane(vehicleID, traci.vehicle.getLaneIndex(vehicleID) + 1, 500)
        elif next_action == 'Stop':
            traci.vehicle.setSpeed(vehicleID, 0)
        elif next_action == 'Go':
            if vehicle.status == "MidTrip":
                traci.vehicle.setMaxSpeed(vehicleID, 22.22)
            else:
                traci.vehicle.setMaxSpeed(vehicleID, 11.11)
        elif next_action == 'Load':
            # Implement loading logic
            passengers_nearby = traci.vehicle.getPersonIDList(vehicleID)
            for passenger_id in passengers_nearby:
                passenger_position = traci.person.getPosition(passenger_id)
                if sumolib.geomhelper.distance(traci.vehicle.getPosition(vehicleID), passenger_position) <= 10:
                    traci.person.appendWalkingStage(passenger_id, [traci.vehicle.getRoadID(vehicleID)])
                    traci.person.moveTo(passenger_id, vehicleID)
        elif next_action == 'Unload':
            # Implement unloading logic
            passengers_on_board = traci.vehicle.getPersonIDList(vehicleID)
            for passenger_id in passengers_on_board:
                passenger_destination = traci.person.getGoal(passenger_id)
                if sumolib.geomhelper.distance(traci.vehicle.getPosition(vehicleID), passenger_destination) <= 10:
                    traci.person.appendWalkingStage(passenger_id, [passenger_destination])
                    traci.vehicle.moveToXY(vehicleID, "", 0, *passenger_destination)
        
    leading_vehicle = traci.vehicle.getLeader(vehicleID, 5)
    if traci.vehicle.getSpeed(vehicleID) == 0 and not is_vehicle_in_front(vehicleID, leading_vehicle, 5):
        if vehicle.status == "MidTrip":
            traci.vehicle.setMaxSpeed(vehicleID, 22.22)
        else:
            traci.vehicle.setMaxSpeed(vehicleID, 11.11)
        traci.vehicle.setSpeed(vehicleID, traci.vehicle.getMaxSpeed(vehicleID))

    #Change UV Stats
    if vehicle.status == "PickUp" or vehicle.status == "DropOff":
        traci.vehicle.setMaxSpeed(vehicleID, 11.11)
    elif vehicle.status == "MidTrip":
        traci.vehicle.setMaxSpeed(vehicleID, 22.22)
    print(vehicle.status)