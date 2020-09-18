from flask import Flask, render_template, request
from BusBoard import BusBoard

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/busInfo")
def busInfo():
    postcode = request.args.get('postcode')
    bus_board = BusBoard(postcode)
    print(bus_board.postcode)
    return render_template('info.html', bus_board=bus_board)

if __name__ == "__main__": app.run()