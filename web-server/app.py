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
    GPIO.output(pins[k], GPIO.LOW)
    time.sleep(1)
    GPIO.output(pins[k], GPIO.HIGH)


# GPIO.output(pins["MAXFAN"], GPIO.LOW)


@app.route('/', methods=["GET"])
def home():
    if(request.method == 'GET'):
        data = {}
        for k in pins.keys():
            data[k] = "on" if GPIO.input(pins[k]) is 0 else "off"

        return jsonify({'data': data})


@app.route('/smarthome/<device>/<action>', methods=['GET'])
def switcher(device, action):
    device_key = device.upper()

    if device_key == "MAXFAN":
        if action == "turn_on":
            GPIO.output(pins[device_key], GPIO.LOW)
        elif action == "turn_off":
            GPIO.output(pins[device_key], GPIO.HIGH)
    else:
        if action == "turn_on":
            GPIO.output(pins[device_key], GPIO.HIGH)
        elif action == "turn_off":
            GPIO.output(pins[device_key], GPIO.LOW)

    return jsonify({"data": f"{device_key} {action} successful!"})


@app.route('/smarthome/<device>/status', methods=['GET'])
def status(device):
    device_key = device.upper()

    if device_key == "MAXFAN":
        data = {"state": "on" if GPIO.input(pins[device_key]) is 0 else "off"}
    else:
        data = {"state": "on" if GPIO.input(pins[device_key]) is 1 else "off"}

    return jsonify(data)


if __name__ == "__main__":
    app.run(port=5600, debug=True)
