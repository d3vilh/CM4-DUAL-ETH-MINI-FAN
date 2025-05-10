# CM4-DUAL-ETH-MINI-FAN
FAN control script for Waveshare CM4 DUAL ETH MINI board.

This script is designed to control a fan speed based on temperature readings.
It uses the GPIO library to interact with the Raspberry Pi's GPIO pins.

The script reads the temperature from a thermal zone file and adjusts the PWM signal to control the fan speed.
It also uses edge detection to measure the fan speed by counting the number of pulses from a fan's tachometer output.
The script runs indefinitely until interrupted by the user (Ctrl+C).
It is important to note that this script requires the RPi.GPIO library to be installed (`sudo apt install python3-gpiozero`) and the script to be run with **root** privileges.

The script is designed to be run on a Raspberry Pi CM4 with a fan connected to the standard Waveshare CM4 DUAL ETHERNET mini board FAN GPIO pins.

## Usage
`sudo python fan-control.py`

## Permanent installation

1. Copy file to `/root/fan-control.py`
2. add line `python /root/fan-control.p` into `/etc/rc.local` right before `exit 0` line:
```bash
sudo sh -c 'grep -q "python /root/fan-control.py" /etc/rc.local || sudo sed -i "/exit 0/i python /root/fan-control.py" /etc/rc.local'
```

It will run in background after the reboot.