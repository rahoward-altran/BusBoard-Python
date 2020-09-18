from datetime import datetime


class Bus:

    def __init__(self, line, aim, time: datetime):
        self.number = line
        self.departure_time = time
        self.aim_time = aim

    def __str__(self):
        return "Number: %s. Time: %s. Aim time: %s" % (self.number,
                                         datetime.strftime(self.departure_time, "%H:%M"),
                                         datetime.strftime(self.aim_time, "%H:%M"))
