from api.amsterdam_api import AmsterdamApi
from api.ns_api import NSApi
from collections import Counter
from time import sleep

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
    print("NS API Test")
    ns_api = NSApi()

    # Get a list of trainstations
    stations = ns_api.get_train_stations()

    # Assignment 1
    # get_disrupted(ns_api, stations)

    # Get all the departure trains from one train station (direction and delay in seconds)
    # Use id from get_train_stations() as identifier.
    # longest_delay = get_longest_delay(ns_api, stations)
    # print("The train highest delay is at station {} with {} seconds delay"
    #             .format(longest_delay['station'], longest_delay['delay']))
 

    # Check how fast the delay will get resolved by printing delays in the next station
    # get_resolved_delay(ns_api, longest_delay)

    find_busiest_station(ns_api, stations)

def get_disrupted(ns_api, stations):
    """ Get the disrupted stations and print information about them """ 
    disrupted_stations_counter = Counter()

    for disruption in ns_api.get_disruptions():
        disrupted_stations_counter.update(disruption['stations'])

    n_stations_disrubted = 100.0 * len(disrupted_stations_counter) / len(stations)
    print("The percentage of stations affected is: {}%".format(n_stations_disrubted))
    print("The top 3 most effected stations are: ")
    for x in disrupted_stations_counter.most_common(3):
        print("  {} with {} disruptions".format(x[0], x[1]))

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
                if len(longest_delay['stations']) > 0: 
                    return longest_delay
       
    return longest_delay

def get_resolved_delay(ns_api, longest_delay):
    for station in longest_delay['stations']:
        print("The next station with id {} has :".format(station))
        for departure in ns_api.get_departures(station):
            if departure['id'] == longest_delay['id']:
                print("{}s".format(departure['delay_seconds']))

def find_busiest_station(ns_api, stations):
    departed_counter = Counter()

    for _ in range(10):
        for station in stations:
            for departure in ns_api.get_departures(station["id"]):
                departed_counter.update(departure['stations'])
        sleep(60)
    
    print(departed_counter.most_common(3))

if __name__ == "__main__":
    main()