from googleplaces import GooglePlaces, types
from operator import itemgetter

from nearby import googleMapsApi

API_KEY = 'AIzaSyDnB2ber8l-M2NuVDfT30PHDT9B6hbJNMw'
google_places = GooglePlaces(api_key=API_KEY)


# ------------------------------------------------ Nearby Schools Data -------------------------------------------------
def schools(post_code):
    print("School ---------------------------------")
    school_names_list = []
    # school_address_list = []
    school_distance_list = []

    query_result = google_places.nearby_search(
        location=post_code, keyword='school', radius=1000, types=[types.TYPE_SCHOOL], rankby='distance')

    for place in query_result.places:
        school_names_list.append(place.name)
        location = place.geo_location
        # print(place.place_id)
        school_distance = googleMapsApi.distance_calc(post_code, location)
        school_distance_list.append(school_distance)
        # place.get_details()
        # school_address_list.append(place.formatted_address)

    print(school_names_list)
    # print(school_address_list)

    return 0
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------- Nearby Transport Data ------------------------------------------------
def transport(post_code):
    transport_train(post_code, 1)
    transport_transit(post_code)
    transport_airport(post_code)


def transport_train(post_code, distance):
    print("Trains ---------------------------------")

    meters = distance * 1609.344

    train_station_list = []
    train_distance_list = []

    query_result = google_places.nearby_search(location=post_code, radius=meters, types=[types.TYPE_TRAIN_STATION,
                                                                                         types.TYPE_SUBWAY_STATION])

    for place in query_result.places:
        station_name = place.name
        if ("Station" or "station") not in station_name:
            station_name += " Station"
        station_distance = googleMapsApi.distance_calc(post_code, place.geo_location)
        if station_distance <= distance:
            train_station_list.append(station_name)
            train_distance_list.append(station_distance)
            print("{0} ({1})".format(station_name, station_distance))

    train_dict = dict(zip(train_station_list, train_distance_list))
    train_dict_sorted = sorted(train_dict.items(), key=itemgetter(1), reverse=False)
    return train_dict_sorted


def transport_transit(post_code):
    print("Buses ----------------------------------")
    query_result = google_places.nearby_search(
        location=post_code, radius=3000, types=[types.TYPE_BUS_STATION], rankby='distance')

    for place in query_result.places[:5]:
        print(place.name)
        location = place.geo_location
        transport_distance = googleMapsApi.distance_calc(post_code, location)
        print(transport_distance)


def transport_airport(post_code):
    print("Airports -------------------------------")
    query_result = google_places.nearby_search(
        location=post_code, name='airport', radius=40000, types=[types.TYPE_AIRPORT], rankby='distance')

    for place in query_result.places:
        print(place.name)
        location = place.geo_location
        distance = googleMapsApi.distance_calc(post_code, location)
        print(distance)
# ----------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------- Nearby Shops Data --------------------------------------------------
def shops(post_code):
    print("Shops ----------------------------------")
    query_result = google_places.nearby_search(
        location=post_code, radius=3000, types=[types.TYPE_STORE], rankby='distance')

    for place in query_result.places:
        print(place.name)
        location = place.geo_location
        distance = googleMapsApi.distance_calc(post_code, location)
        print(distance)
# ----------------------------------------------------------------------------------------------------------------------
