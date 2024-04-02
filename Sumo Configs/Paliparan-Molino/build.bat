python "%SUMO_HOME%\tools\randomTrips.py" -n osm.net.xml.gz --fringe-factor 2 --insertion-density 6 -o osm.bicycle.trips.xml -r osm.bicycle.rou.xml -b 0 -e 3600 --trip-attributes "departLane=\"best\"" --fringe-start-attributes "departSpeed=\"max\"" --validate --remove-loops --via-edge-types highway.motorway,highway.motorway_link,highway.trunk_link,highway.primary_link,highway.secondary_link,highway.tertiary_link --vehicle-class bicycle --vclass bicycle --prefix bike --max-distance 8000
python "%SUMO_HOME%\tools\randomTrips.py" -n osm.net.xml.gz --fringe-factor 5 --insertion-density 4 -o osm.bus.trips.xml -r osm.bus.rou.xml -b 0 -e 3600 --trip-attributes "departLane=\"best\"" --fringe-start-attributes "departSpeed=\"max\"" --validate --remove-loops --via-edge-types highway.motorway,highway.motorway_link,highway.trunk_link,highway.primary_link,highway.secondary_link,highway.tertiary_link --vehicle-class bus --vclass bus --prefix bus --min-distance 600 --min-distance.fringe 10
python "%SUMO_HOME%\tools\randomTrips.py" -n osm.net.xml.gz --fringe-factor 2 --insertion-density 4 -o osm.motorcycle.trips.xml -r osm.motorcycle.rou.xml -b 0 -e 3600 --trip-attributes "departLane=\"best\"" --fringe-start-attributes "departSpeed=\"max\"" --validate --remove-loops --via-edge-types highway.motorway,highway.motorway_link,highway.trunk_link,highway.primary_link,highway.secondary_link,highway.tertiary_link --vehicle-class motorcycle --vclass motorcycle --prefix motorcycle --max-distance 1200
python "%SUMO_HOME%\tools\randomTrips.py" -n osm.net.xml.gz --fringe-factor 5 --insertion-density 12 -o osm.passenger.trips.xml -r osm.passenger.rou.xml -b 0 -e 3600 --trip-attributes "departLane=\"best\"" --fringe-start-attributes "departSpeed=\"max\"" --validate --remove-loops --via-edge-types highway.motorway,highway.motorway_link,highway.trunk_link,highway.primary_link,highway.secondary_link,highway.tertiary_link --vehicle-class passenger --vclass passenger --prefix veh --min-distance 300 --min-distance.fringe 10 --allow-fringe.min-length 1000 --lanes
