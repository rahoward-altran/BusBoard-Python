import requests
import json

from BusStop import BusStop

NEAREST_BUSES_REQUEST = 'https://transportapi.com/v3/uk/bus/stop/%s/live.json?app_id=%s&app_key=%s&group=route&nextbuses=yes'
GET_STOP_CODE_REQUEST = "https://transportapi.com/v3/uk/bus/stops/near.json?app_id=%s&app_key=%s&lat=%f&lon=%f"
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
    app_key, app_id = get_key_and_id()
    bus_stop_response = requests.get(
        GET_STOP_CODE_REQUEST % (app_id, app_key, location_info["latitude"], location_info["longitude"]))
    bus_stop_dict = json.loads(bus_stop_response.text)
    return bus_stop_dict["stops"]


def get_key_and_id():
    with open("keys/keys.json") as json_file:
        json_data = json.load(json_file)
        return json_data["app_key"], json_data["app_id"]


def get_location_info_from_postcode():
    get_user_input = True
    while get_user_input:
        postcode_input = input("Please enter a postcode: ")

        postcode_response = requests.get(POSTCODES_REQUEST % (postcode_input))

        get_user_input = not postcode_response.ok

    postcode_dict = json.loads(postcode_response.text)
    return postcode_dict["result"]


def get_next_buses(stop_code):
    app_key, app_id = get_key_and_id()
    response = requests.get(NEAREST_BUSES_REQUEST % (stop_code, app_id, app_key))
    return response


def add_timetable_to_stops(stops):
    for stop in stops:
        response = get_next_buses(stop.atcocode)
        next_buses_dict = json.loads(response.text)

        stop.populate_buses(next_buses_dict["departures"])


def print_stops(stops):
    for stop in stops:
        stop.print_timetable()


if __name__ == "__main__":
    main()
