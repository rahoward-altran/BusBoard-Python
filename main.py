import requests
import ast
import json

from BusStop import BusStop
from Timetable import Timetable

NEAREST_BUSES_REQUEST = 'https://transportapi.com/v3/uk/bus/stop/%s/live.json?app_id=af190c09&app_key=ff4d33b5a814fbe2ee7ba49fd63312cb&group=route&nextbuses=yes'
GET_STOP_CODE_REQUEST = "https://transportapi.com/v3/uk/bus/stops/near.json?app_id=e1420c74&app_key=11fcf40bd3749dfe5bd2de752e3a7294&lat=%s&lon=%s"
POSTCODES_REQUEST = "http://api.postcodes.io/postcodes/%s"

def main():
    print("Welcome to BusBoard.")

    nearest_stops = get_stops_from_postcode()

    add_timetable_to_stops(nearest_stops)

    print_stops(nearest_stops)


def get_stops_from_postcode():
    location_info = get_location_info_from_postcode()

    bus_stop_data = get_bus_stop_data_from_location(location_info)

    stops = []
    stop_count = 0

    for stop in bus_stop_data:
        stops.append(BusStop(stop))
        stop_count += 1
        if stop_count == 2:
            break
    return stops


def get_bus_stop_data_from_location(location_info):
    bus_stop_response = requests.get(GET_STOP_CODE_REQUEST % (str(location_info["latitude"]),
                                                              str(location_info["longitude"])))
    return ast.literal_eval(bus_stop_response.text)["stops"]


def get_location_info_from_postcode():
    get_user_input = True
    while get_user_input:
        postcode_input = input("Please enter a postcode: ")

        postcode_response = requests.get(POSTCODES_REQUEST % postcode_input)

        get_user_input = not postcode_response.ok

    postcode_json_string = postcode_response.text.replace("'", "\"")
    postcode_dict = json.loads(postcode_json_string)
    return postcode_dict["result"]


def get_next_buses(stop_code):
    response = requests.get(NEAREST_BUSES_REQUEST % stop_code)
    return response


def add_timetable_to_stops(stops):
    for stop in stops:
        response = get_next_buses(stop.atcocode)
        next_buses_dict = ast.literal_eval(response.text)

        departures = next_buses_dict['departures']
        stop.timetable = Timetable(stop.name, departures)


def print_stops(stops):
    for stop in stops:
        stop.print_timetable()


if __name__ == "__main__":
    main()
