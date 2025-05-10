# v.0.2 by d3vilh 2025. 
# This script is designed to control a fan speed based on temperature readings.
# It uses the GPIO library to interact with the Raspberry Pi's GPIO pins.
# The script reads the temperature from a thermal zone file and adjusts the PWM signal to control the fan speed. 
# It also uses edge detection to measure the fan speed by counting the number of pulses from a fan's tachometer output.
# The script runs indefinitely until interrupted by the user (Ctrl+C).
# It is important to note that this script requires the RPi.GPIO library to be installed and the script to be run with root privileges.
# The script is designed to be run on a Raspberry Pi with a fan connected to the specified GPIO pins.
#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

pwmPin = 19        # GPIO pin for PWM signal
fgPin = 17         # GPIO pin for fan tachometer signal
freq = 1000        # Frequency for PWM signal
dc = 50            # Initial duty cycle for PWM signal (50% FAN duty cycle)
onGetSpeed = False # Flag to indicate if edge detection is active
t1 = 0             # Last time the tachometer signal was detected
t = 1              # Time interval for speed calculation

def startGetSpeed():
    global onGetSpeed
    try:
        GPIO.add_event_detect(fgPin, GPIO.FALLING, callback=speedcallback)
        onGetSpeed = True
        print("Edge detection started") # Debugging print
    except RuntimeError as e:
        print(f"Error starting edge detection: {e}")  # More informative error message

def stopGetSpeed():
    global onGetSpeed
    if onGetSpeed: # Only remove if it was actually started.
        GPIO.remove_event_detect(fgPin)
        onGetSpeed = False
        print("Edge detection stopped") # Debugging print

def speedcallback(channel):
    global t1, t
    if t1 != 0:
        t = time.time() - t1
        t1 = 0
    else:
        t1 = time.time()

def getTemp():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        return int(f.read()) / 1000.0

def autoSpeed(dc, temp):
    if temp < 40 and dc >= 10:    # Avoid negative duty cycle
        return dc - 10            # Decrease duty cycle
    elif temp > 42 and dc <= 90:  # Avoid exceeding 100% duty cycle
        return dc + 10            # Increase duty cycle
    else:
        return dc

if __name__ == '__main__':
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pwmPin, GPIO.OUT)
    GPIO.setup(fgPin, GPIO.IN)
    pwm = GPIO.PWM(pwmPin, freq)
    pwm.start(dc)

    try:
        startGetSpeed()
        num = 10
        while True:
            speed = 60 / (t * 2) if t != 0 else 0  # Avoid division by zero
            temp = getTemp()
            print("Speed: %f RPM" % speed)
            print("Temp: %f °C" % temp)
            print("\33[3A")  # Clear previous line

            if num > 5:
                num = 0
                dc = autoSpeed(dc, temp)
                pwm.ChangeDutyCycle(dc)
            num += 1
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        stopGetSpeed()
        pwm.stop()
        GPIO.cleanup()