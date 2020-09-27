import RPi.GPIO as GPIO
from flask import Flask, request, jsonify
import time

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

pins = {
    "TUBELIGHT": 2,
    "FAN": 3,
    "MAXFAN": 4,
    "LOOSE": 14
}

for k in pins.keys():
    GPIO.setup(pins[k], GPIO.OUT)
    GPIO.setup(pins[k], GPIO.LOW)
    time.sleep(2)
    GPIO.setup(pins[k], GPIO.HIGH)


@app.route('/', methods=["GET"])
def home():
    if(request.method == 'GET'):
        data = {}
        for k in pins.keys():
            data[k] = "on" if GPIO.input(pins[k]) is 0 else "off"

        return jsonify({'data': data})

@app.route('/smarthome/<device>/<action>', methods=['GET'])
def switcher(device, action):
    pass

@app.route('/smarthome/<device>/status', methods=['GET'])
def status(device):
    device_key = device.lower()

    data = {
        "state": "on" if GPIO.input(pins[device_key]) is 0 else "off"
    }

    return jsonify(data)