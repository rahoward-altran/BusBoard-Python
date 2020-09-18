class BusStop:
    def __init__(self, stop_dictionary):
        self.atcocode = stop_dictionary["atcocode"]
        self.name = stop_dictionary["name"]
        self.timetable = 0

    def print_timetable(self):
        print(self.name)
        self.timetable.print_first_five()
