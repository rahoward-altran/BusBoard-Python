import requests
import ast
from Timetable import Timetable

GET_STOP_CODE_REQUEST = "https://transportapi.com/v3/uk/bus/stops/near.json?app_id=e1420c74&app_key=11fcf40bd3749dfe5bd2de752e3a7294&lat=%s&lon=%s"

def main():

    # get_stop_from_postcode()

    print("Welcome to BusBoard.")
    response = get_next_buses()

    # #490000077D
    text = response.content.decode("utf-8")

    dict = ast.literal_eval(response.content.decode("utf-8"))

    departures = dict['departures']
    timetable = Timetable(departures)

    timetable.sort_buses()
    timetable.print_first_five()


def get_stop_from_postcode():
    postcode = "se249nw"

    response = requests.get("http://api.postcodes.io/postcodes/%s" % postcode)

    text = response.text
    response_decoded = ast.literal_eval(text)
    result = response_decoded["result"]


    bus_stop_respose = requests.get(GET_STOP_CODE_REQUEST & (result["latitude"], result["longitude"]))

    nearest_stop = ast.literal_eval(bus_stop_respose.content.decode("utf-8"))["stops"][0]["atcocode"]
    return nearest_stop


def get_next_buses():
    user_input = input("Please give a buss stop code: ")
    response = requests.get(
        'https://transportapi.com/v3/uk/bus/stop/%s/live.json?app_id=af190c09&app_key=ff4d33b5a814fbe2ee7ba49fd63312cb&group=route&nextbuses=yes' % user_input)
    if not response.ok:
        get_next_buses()
    return response


if __name__ == "__main__":
    main()
