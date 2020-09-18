import requests
import json
from BusStop import BusStop

NEAREST_BUSES_REQUEST = 'https://transportapi.com/v3/uk/bus/stop/%s/live.json?app_id=%s&app_key=%s&group=route&nextbuses=yes'
GET_STOP_CODE_REQUEST = "https://transportapi.com/v3/uk/bus/stops/near.json?app_id=%s&app_key=%s&lat=%f&lon=%f"
POSTCODES_REQUEST = "http://api.postcodes.io/postcodes/%s"


class BusBoard:
    def __init__(self, postcode):
        self.postcode = postcode
        self.bus_stops = self.get_stops_from_postcode()
        self.add_timetable_to_stops()

    def get_stops_from_postcode(self):
        location_info = self.get_location_info_from_postcode(self.postcode)
        bus_stop_data = self.get_bus_stop_data_from_location(location_info)

        stops = []
        stop_count = 0

        for stop in bus_stop_data:
            stops.append(BusStop(stop))
            stop_count += 1
            if stop_count == 2:
                break
        return stops

    def get_bus_stop_data_from_location(self, location_info):
        app_key, app_id = self.get_key_and_id()
        bus_stop_response = requests.get(
            GET_STOP_CODE_REQUEST % (app_id, app_key, location_info["latitude"], location_info["longitude"]))
        bus_stop_dict = json.loads(bus_stop_response.text)
        return bus_stop_dict["stops"]

    def get_key_and_id(self):
        with open("keys/keys.json") as json_file:
            json_data = json.load(json_file)
            return json_data["app_key"], json_data["app_id"]

    def get_location_info_from_postcode(self, postcode):
        postcode_response = requests.get(POSTCODES_REQUEST % postcode)
        postcode_dict = json.loads(postcode_response.text)
        return postcode_dict["result"]

    def get_next_buses(self, stop_code):
        app_key, app_id = get_key_and_id()
        response = requests.get(NEAREST_BUSES_REQUEST % (stop_code, app_id, app_key))
        return response

    def add_timetable_to_stops(self):
        for stop in self.bus_stops:
            response = self.get_next_buses(stop.atcocode)
            next_buses_dict = json.loads(response.text)

            stop.populate_buses(next_buses_dict["departures"])
    #
    # def print_stops(self, stops):
    #     for stop in stops:
    #         stop.print_timetable()

