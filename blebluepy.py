from bluepy.btle import Scanner

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

scanner = Scanner()

beacon_miss_cntr = 0

while True:
	bandcontrol = True if GPIO.input(20) is 1 else False
	print("Band Control is %s" % bandcontrol)
	print("Device Miss Counter: " + str(beacon_miss_cntr))

	devices = scanner.scan(1)

	found_flag = 0
	
	if len(devices) > 0:
		for dev in devices:
			print("Device %s, RSSI=%d dB" % (dev.addr, dev.rssi))
			
			if dev.addr == "dd:96:f1:1d:1b:1e":
				print("Band Found")
				
				if dev.rssi > -80:
					
					print("Band in Range")
					found_flag = 1

					print("Device Entered! Resetting Counter......")
					beacon_miss_cntr = 0
					
					if bandcontrol:
						print("Turning On Devices.....")
						turn_on_devices()

	if not found_flag:
		beacon_miss_cntr = beacon_miss_cntr + 1
		print("Device Missed! Increasing Counter......")
	
	if bandcontrol and beacon_miss_cntr > 15:
		print("Empty Room! Turning Off Devices......")
		turn_off_devices()
