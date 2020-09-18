from datetime import datetime

from Bus import Bus


class BusStop:
    def __init__(self, stop_dictionary):
        self.atcocode = stop_dictionary["atcocode"]
        self.name = stop_dictionary["name"] + " " + stop_dictionary["indicator"]
        self.buses = []

    def print_timetable(self):
        print(self.name)
        self.print_first_five()

    def populate_buses(self, departures):
        count = 0
        for bus_route_name, bus_info in departures.items():
            for bus in bus_info:
                if count == 5:
                    break
                count += 1
                est_date = bus['expected_departure_date']
                est_time = bus['best_departure_estimate']
                aim_time = bus['aimed_departure_time']
                try:
                    departure_time = datetime.strptime(est_date + " " + est_time, "%Y-%m-%d %H:%M")
                    aim = datetime.strptime(est_date + " " + aim_time, "%Y-%m-%d %H:%M")
                    self.buses.append(Bus(bus['line'], aim, departure_time))
                except:
                    pass

    def sort_buses(self):
        self.buses.sort(key=lambda bus: bus.departure_time)

    def print_first_five(self):
        for bus in self.buses[0:5]:
            print(bus)
