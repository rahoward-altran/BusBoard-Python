from datetime import datetime

from Bus import Bus


class Timetable:
    def __init__(self, stop_name, departures):
        self.stop_name = stop_name
        self.buses = []
        self.departures = departures
        self.populate_timetable()

    def sort_buses(self):
        self.buses.sort(key=lambda bus: bus.departure_time)

    def print_first_five(self):
        for bus in self.buses[0:5]:
            print(bus)

    def populate_timetable(self):
        for bus_route_name, bus_info in self.departures.items():
            for bus in bus_info:
                est_date = bus['expected_departure_date']
                est_time = bus['best_departure_estimate']
                departure_time = datetime.strptime(est_date + " " + est_time, "%Y-%m-%d %H:%M")
                self.buses.append(Bus(bus['line'], departure_time))
