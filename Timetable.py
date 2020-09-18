from datetime import datetime

from Bus import Bus


class Timetable:
    # buses: List[Bus]

    def __init__(self, departures):
        self.buses = []
        self.departures = departures
        self.populate_timetable()

    def sort_buses(self):
        self.buses.sort(key=lambda bus: bus.departure_time)

    def print_first_five(self):
        for bus in self.buses[0:5]:
            print(bus)
    # all_buses: List[Bus]

    def populate_timetable(self):
        for bus_route_name, bus_info in self.departures.items():
            for bus in bus_info:
                # ToDo:
                est_date = bus['expected_departure_date']
                est_time = bus['best_departure_estimate']
                departure_time = datetime.strptime(est_date + " " + est_time, "%Y-%m-%d %H:%M")
                # print(departure_time)
                number = bus['line']
                # print(number)
                new_bus = Bus(number, departure_time)
                # new_bus = Bus(departure_time)
                self.buses.append(new_bus)
