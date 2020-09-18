from datetime import datetime

from Bus import Bus


class BusStop:
    def __init__(self, stop_dictionary):
        self.atcocode = stop_dictionary["atcocode"]
        self.name = stop_dictionary["name"]
        self.buses = []

    def print_timetable(self):
        print(self.name)
        self.print_first_five()

    def populate_buses(self, departures):
        for bus_route_name, bus_info in departures.items():
            for bus in bus_info:
                est_date = bus['expected_departure_date']
                est_time = bus['best_departure_estimate']
                departure_time = datetime.strptime(est_date + " " + est_time, "%Y-%m-%d %H:%M")
                self.buses.append(Bus(bus['line'], departure_time))

    def sort_buses(self):
        self.buses.sort(key=lambda bus: bus.departure_time)

    def print_first_five(self):
        for bus in self.buses[0:5]:
            print(bus)
