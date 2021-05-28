from bluetooth.ble import DiscoveryService

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)

def turn_off_devices():
    GPIO.output(2, GPIO.LOW)
    GPIO.output(3, GPIO.LOW)
    GPIO.output(14, GPIO.HIGH)
    # GPIO.output(4, GPIO.LOW)

def turn_on_devices():
    GPIO.output(2, GPIO.HIGH)
    GPIO.output(3, GPIO.HIGH)
    GPIO.output(4, GPIO.HIGH)


service = DiscoveryService()

beacon_miss_cntr = 0

while True:

    bandcontrol = True if GPIO.input(20) is 1 else False
    print("Band Control is %s" % bandcontrol)

    print("Device Miss Counter: " + str(beacon_miss_cntr))
    
    devices = service.discover(2)

    print(devices)

    if not "DD:96:F1:1D:1B:1E" in devices.keys():
        print("Device Missed! Increasing Counter......")
        beacon_miss_cntr = beacon_miss_cntr + 1

    else:
        print("Device Entered! Resetting Counter......")
        beacon_miss_cntr = 0

        print("Turning On Devices.....")
        turn_on_devices()

    if bandcontrol and beacon_miss_cntr > 10:
        print("Empty Room! Turning Off Devices......")
        turn_off_devices()