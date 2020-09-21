from datetime import datetime


class Bus:

    def __init__(self, line, aim, time: datetime):
        self.number = line
        self.departure_time = time
        self.aim_time = aim
        if type(self.departure_time) is datetime:
            self.mins_to_departure = int((self.departure_time - datetime.now()).total_seconds() / 60.0)
        else:
            self.mins_to_departure = "N/A"

    def __str__(self):
        return "Number: %s. Time: %s. Aim time: %s." % (self.number, self.get_departure_time(), self.get_aim_time())

    def get_departure_time(self):
        if type(self.departure_time) is datetime:
            return datetime.strftime(self.departure_time, "%H:%M")
        return self.departure_time

    def get_aim_time(self):
        if type(self.aim_time) is datetime:
            return datetime.strftime(self.aim_time, "%H:%M")
        return self.aim_time
