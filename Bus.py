from datetime import datetime


class Bus:

    def __init__(self, line, time: datetime):
        self.number = line
        self.departure_time = time

    def __str__(self):
        return "Number: %s. Time: %s" % (self.number, datetime.strftime(self.departure_time, "%H:%M"))
