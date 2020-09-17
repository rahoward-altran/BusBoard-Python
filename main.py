import requests
import json
import ast
from typing import List, Type
from _datetime import datetime


class Bus:

    def __init__(self, time: datetime):
        #self.number = line
        self.departure_time = time


class TimeTable:
    # buses: List[Bus]

    def __init__(self):
        self.buses = []

    # all_buses: List[Bus]
#-------------------------------------------------------


def main():
    print("Welcome to BusBoard.")
    # user_input = input("Please give a buss stop code: ")

    # ToDo DESIGN: request userinputed bus stop info from api
    #response = requests.get('https://transportapi.com/v3/uk/bus/stop/'+user_input+'/live.json?app_id=af190c09&app_key=ff4d33b5a814fbe2ee7ba49fd63312cb&group=route&nextbuses=yes')
    response = requests.get('https://transportapi.com/v3/uk/bus/stop/490000077D/live.json?app_id=af190c09&app_key=ff4d33b5a814fbe2ee7ba49fd63312cb&group=route&nextbuses=yes')
    dict = ast.literal_eval(response.content.decode("utf-8"))

    timetable: Type[TimeTable] = TimeTable()

    # ToDo DESIGN interpret the json response
    departures = dict['departures']
    for bus_route_name, bus_info in departures.items():
        for bus in bus_info:
            # ToDo:
            est_date = bus['expected_departure_date']
            est_time = bus['best_departure_estimate']
            departure_time = datetime.strptime(est_date + " " + est_time, "%Y-%m-%d %H:%M")
            print(departure_time)
            number = bus['line']
            print(number)
            #new_bus = Bus(number, departure_time)
            new_bus = Bus(departure_time)
            timetable.buses.append(new_bus)

    print(timetable.buses)
    #ToDo CODE sort through the list of type Bus by departure time
    # all_buses.sort(key=lambda bus : bus['best_departure_estimate'])
    # for bus in all_buses:
    #     print(bus['best_departure_estimate'])


    # ToDo DESIGN print out the next 5 busses at the stop


if __name__ == "__main__": main()