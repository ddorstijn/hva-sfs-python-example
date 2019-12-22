from api.amsterdam_api import AmsterdamApi
from api.ns_api import NSApi

# Assignment 1 and 4
from collections import Counter
# Assignment 4
from time import sleep

# Assignment 5
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def trash_bins():
    amsterdam_api = AmsterdamApi()
    list_trash_bins = amsterdam_api.get_trash_bins()

    print("Overview of trash bins in Amsterdam")

    for trash_bin in list_trash_bins:
        print(
            str(trash_bin['id']) + "\t" +
            trash_bin['name'] + "\t" +
            trash_bin['type'] + "\t" +
            trash_bin['address']
        )

def main():
    print("NS API Assignments")
    ns_api = NSApi()

    # Get a list of trainstations
    stations = ns_api.get_train_stations()

    # Assignment 1
    get_disrupted(ns_api, stations)

    # Assignment 2
    longest_delay = get_longest_delay(ns_api, stations)
    print("The train highest delay is at station {} with {} seconds delay"
                .format(longest_delay['station'], longest_delay['delay']))

    # Assignment 3
    get_resolved_delay(ns_api, longest_delay)

    # Assignment 4 
    find_busiest_station(ns_api, stations)

    # Assignment 5
    draw_stations_map(stations)

def get_disrupted(ns_api, stations):
    """ Get the disrupted stations and print information about them """ 
    disrupted_stations_counter = Counter()

    for disruption in ns_api.get_disruptions():
        disrupted_stations_counter.update(disruption['stations'])

    n_stations_disrubted = 100.0 * len(disrupted_stations_counter) / len(stations)
    print("The percentage of stations affected is: {}%".format(n_stations_disrubted))
    print("The top 3 most effected stations are: ")
    for x in disrupted_stations_counter.most_common(3):
        station_name = find_station_from_code(stations, x[0])['name']
        print("  {} with {} disruptions".format(station_name, x[1]))

def get_longest_delay(ns_api, stations):
    """ Get the longest delayed train departure """
    longest_delay = {'id': 0, 'delay': 0, 'station': "", 'stations': []} 
    
    for station in stations:
        for departure in ns_api.get_departures(station["id"]):
            if departure['delay_seconds'] > longest_delay['delay']:
                longest_delay['id'] = departure['id']
                longest_delay['delay'] = departure['delay_seconds']
                longest_delay['station'] = station['name']
                longest_delay['stations'] = departure['stations']
       
    return longest_delay

def get_resolved_delay(ns_api, longest_delay):
    """ Check if the delay gets resolved further along the route """
    for station in longest_delay['stations']:
        print("The next station with id {} has :".format(station))
        for departure in ns_api.get_departures(station):
            if departure['id'] == longest_delay['id']:
                print("{}s".format(departure['delay_seconds']))

def find_busiest_station(ns_api, stations):
    """ Track train departures over time to see what station is the busiest """
    departed_counter = Counter()

    # Check 6 times in total
    for _ in range(6):
        print("Looking through stations")
        for station in stations:
            for departure in ns_api.get_departures(station["id"]):
                departed_counter.update(departure['stations'])
        print("Waiting for a bit before checking again.")
        # Sleep for 45 minutes
        sleep(3600 * .75)
    
    for station_id, counter in departed_counter.most_common(3):
        station = find_station_from_id(stations, station_id)
        print("The busiest station is {} with a total of {} trains tracked.".format(station['name'], counter))

def find_station_from_id(stations, id):
    """ Return the station object from it's id """
    for station in stations:
        if station['id'] == id:
            return station

def find_station_from_code(stations, code):
    """ Return the station object from it's code """
    for station in stations:
        if station['code'] == code:
            return station

def draw_stations_map(stations):
    station_coords = [s['location'] for s in stations]
    df = pd.DataFrame(station_coords)
    bbox = ((df.lng.min(), df.lng.max(), df.lat.min(), df.lat.max()))
    nl_map = plt.imread('NetherlandsRail.png')
    
    fig, ax = plt.subplots(figsize = (6.5,8))
    ax.scatter(df.lng, df.lat, zorder=1, alpha= 0.5, c='b', s=10)
    ax.set_title("Map of the Netherlands' different stations")
    ax.set_xlim(bbox[0],bbox[1])
    ax.set_ylim(bbox[2],bbox[3])

    ax.imshow(nl_map, zorder=0, extent = bbox, aspect= 'equal')
    plt.show()

if __name__ == "__main__":
    main()