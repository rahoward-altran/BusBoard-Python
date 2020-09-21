from datetime import datetime

from Bus import Bus


class BusStop:
    def __init__(self, stop_dictionary):
        self.atcocode = stop_dictionary["atcocode"]
        self.name = stop_dictionary["name"] + ", " + stop_dictionary["indicator"]
        self.buses = []
        self.distance = stop_dictionary["distance"]

    def print_timetable(self):
        print(self.name)
        self.print_first_five()

    def populate_buses(self, departures):
        for bus_route_name, bus_info in departures.items():
            for bus in bus_info:
                est_date = bus['expected_departure_date']
                est_time = bus['best_departure_estimate']
                aim_time = bus['aimed_departure_time']

                if est_date is None:
                    est_date = bus['date']
                if est_time is None:
                    est_time = bus['expected_departure_estimate']
                departure_time = self.create_datetime_if_valid(est_date, est_time)
                aim_time = self.create_datetime_if_valid(est_date, aim_time)
                
                self.buses.append(Bus(bus['line'], aim_time, departure_time))
        self.sort_buses()
        del self.buses[5:len(self.buses)]

    @staticmethod
    def create_datetime_if_valid(date, time):
        try:
            time = datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M")
        except TypeError:
            time = "Not found"
        return time

    def sort_buses(self):
        self.buses.sort(key=lambda bus: bus.departure_time)

    def print_first_five(self):
        for bus in self.buses[0:5]:
            print(bus)
