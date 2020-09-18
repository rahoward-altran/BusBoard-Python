import requests
import json
from BusStop import BusStop

NEAREST_BUSES_REQUEST = 'https://transportapi.com/v3/uk/bus/stop/%s/live.json?app_id=%s' \
                        '&app_key=%s&group=route&nextbuses=yes'
GET_STOP_CODE_REQUEST = "https://transportapi.com/v3/uk/bus/stops/near.json?app_id=%s&app_key=%s&lat=%f&lon=%f"
POSTCODES_REQUEST = "http://api.postcodes.io/postcodes/%s"
NUM_STOPS_TO_DISPLAY = 2


class BusBoard:
    def __init__(self, postcode):
        self.app_key, self.app_id = self.get_key_and_id()
        self.postcode = postcode
        self.errors = []
        self.bus_stops = self.get_stops_from_postcode()

    def refresh(self):
        for stop in self.bus_stops:
            stop.buses.clear()
        if len(self.errors) == 0:
            self.add_timetable_to_stops()

    def get_stops_from_postcode(self):
        try:
            location_info = self.get_location_info_from_postcode()
        except:
            self.errors.append("Postcode: %s is not valid." % self.postcode)
            return
        try:
            bus_stop_data = self.get_bus_stop_data_from_location(location_info)
        except:
            self.errors.append("Could not get bus stop data from %s." % self.postcode)
            return
        stops = []
        stop_count = 0

        for stop in bus_stop_data:
            stops.append(BusStop(stop))
            stop_count += 1
            if stop_count == NUM_STOPS_TO_DISPLAY:
                break
        return stops

    def get_bus_stop_data_from_location(self, location_info):
        bus_stop_response = requests.get(
            GET_STOP_CODE_REQUEST % (self.app_id, self.app_key, location_info["latitude"], location_info["longitude"]))
        bus_stop_dict = json.loads(bus_stop_response.text)
        return bus_stop_dict["stops"]

    @staticmethod
    def get_key_and_id():
        with open("keys/keys.json") as json_file:
            json_data = json.load(json_file)
            return json_data["app_key"], json_data["app_id"]

    def get_location_info_from_postcode(self):
        postcode_response = requests.get(POSTCODES_REQUEST % self.postcode)
        postcode_dict = json.loads(postcode_response.text)
        return postcode_dict["result"]

    def get_next_buses(self, stop_code):
        response = requests.get(NEAREST_BUSES_REQUEST % (stop_code, self.app_id, self.app_key))
        return response

    def add_timetable_to_stops(self):
        for stop in self.bus_stops:
            response = self.get_next_buses(stop.atcocode)
            next_buses_dict = json.loads(response.text)
            stop.populate_buses(next_buses_dict["departures"])

    def num_errors(self):
        return len(self.errors)
