from datetime import datetime


class Bus:

    def __init__(self, line, time: datetime):
        self.number = int(line)
        self.departure_time = time

    def __str__(self):
        return "Number: %d. Time: %s" % (self.number, datetime.strftime(self.departure_time, "%H:%M"))