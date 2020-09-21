import requests
import json
from BusStop import BusStop

NEAREST_BUSES_REQUEST = 'https://transportapi.com/v3/uk/bus/stop/%s/live.json'
GET_STOP_CODE_REQUEST = "https://transportapi.com/v3/uk/bus/stops/near.json"
POSTCODES_REQUEST = "https://api.postcodes.io/postcodes/%s"


class BusBoard:
    def __init__(self, postcode, max_distance):
        self.max_distance = int(max_distance)
        self.app_key, self.app_id = self.get_key_and_id()
        self.postcode = postcode
        self.errors = []
        self.bus_stops = self.get_stops_from_postcode()

    def refresh(self):
        for stop in self.bus_stops:
            stop.buses.clear()
        if len(self.errors) == 0:
            self.add_timetable_to_stops()
        return ""

    def get_stops_from_postcode(self):
        try:
            location_info = self.get_location_info_from_postcode()
        except ValueError:
            self.errors.append("Could not get user location from postcode: \"%s\"." % self.postcode)
            return
        try:
            bus_stop_data = self.get_bus_stop_data_from_location(location_info)
        except ValueError:
            self.errors.append("Could not get bus stop data from \"%s\"." % self.postcode)
            return

        stops = []
        for stop in bus_stop_data:
            if int(stop["distance"]) > self.max_distance:
                break
            stops.append(BusStop(stop))
        return stops

    def get_bus_stop_data_from_location(self, location_info):
        bus_stop_response = requests.get(GET_STOP_CODE_REQUEST, params={'api_key': self.app_key, 'app_id': self.app_id,
                                                                        'lat': location_info["latitude"],
                                                                        'lon': location_info["longitude"]})

        bus_stop_dict = json.loads(bus_stop_response.text)
        if not bus_stop_response.ok:
            raise ValueError
        return bus_stop_dict["stops"]

    @staticmethod
    def get_key_and_id():
        with open("keys/keys.json") as json_file:
            json_data = json.load(json_file)
            return json_data["app_key"], json_data["app_id"]

    def get_location_info_from_postcode(self):
        postcode_response = requests.get(POSTCODES_REQUEST % self.postcode)
        postcode_dict = json.loads(postcode_response.text)
        if not postcode_response.ok:
            raise ValueError

        return postcode_dict["result"]

    def get_next_buses(self, stop_code):
        response = requests.get(NEAREST_BUSES_REQUEST % stop_code, params={'nextbuses': 'yes', 'group': 'route',
                                                                           'app_id': self.app_id,
                                                                           'app_key': self.app_key})
        return response

    def add_timetable_to_stops(self):
        for stop in self.bus_stops:
            try:
                response = self.get_next_buses(stop.atcocode)
                next_buses_dict = json.loads(response.text)
                stop.populate_buses(next_buses_dict["departures"])
                if not response.ok:
                    raise ValueError
            except ValueError:
                self.errors.append("Could not get bus data from bus code.")

    def num_errors(self):
        return len(self.errors)
