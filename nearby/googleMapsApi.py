from googlemaps.client import Client
from googlemaps.distance_matrix import distance_matrix
from googlemaps.directions import directions

API_KEY = 'AIzaSyDnB2ber8l-M2NuVDfT30PHDT9B6hbJNMw'
g_maps = Client(API_KEY)


def distance_calc(origin, destination):
    data = distance_matrix(g_maps, origin, destination, units="imperial")
    distance = data['rows'][0]['elements'][0]['distance']['text']
    distance = float(distance[:-3])
    return distance


def directions_calc_train(origin, destination):
    data = directions(g_maps, origin, destination, mode="transit")
    direction_data_duration = data[0]['legs'][0]['duration']['text']
    direction_data_line_type = data[0]['legs'][0]['steps'][0]['transit_details']['line']['short_name']
    direction_data_dict = {direction_data_line_type: direction_data_duration[:-5]}
    return direction_data_dict
