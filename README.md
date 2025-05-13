# CM4-DUAL-ETH-MINI-FAN
FAN control script for [**Waveshare CM4 DUAL ETH MINI board**](https://www.waveshare.com/cm4-dual-eth-mini.htm).

This script is designed to control a fan speed based on temperature readings.
It uses the GPIO library to interact with the Raspberry Pi's GPIO pins.

The script reads the temperature from a thermal zone file and adjusts the PWM signal to control the fan speed.
It also uses edge detection to measure the fan speed by counting the number of pulses from a fan's tachometer output.
The script runs indefinitely until interrupted by the user (Ctrl+C).
It is important to note that this script requires the RPi.GPIO library to be installed (`sudo apt install python3-gpiozero`) and the script to be run with **root** privileges.

The script is designed to be run on a Raspberry Pi CM4 with a fan connected to the standard [**Waveshare CM4 DUAL ETHERNET mini board**](https://www.waveshare.com/wiki/CM4-DUAL-ETH-MINI) FAN GPIO pins.

CPU temp graph on CM4 after applying script:

![FAN running graph after script execution](/FAN-Graph.png) 

## Usage
`sudo python fan-control.py`

## Permanent installation

1. Copy file to `/root/fan-control.py`
2. add line `python /root/fan-control.py` into `/etc/rc.local` right before `exit 0` line:
```bash
sudo sh -c 'grep -q "python /root/fan-control.py" /etc/rc.local || sudo sed -i "/exit 0/i python /root/fan-control.py" /etc/rc.local'
```

It will run in background after the reboot.


<a href="https://www.buymeacoffee.com/d3vilh" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="51" width="217"></a>

May 2025, [**d3vilh**](https://github.com/d3vilh)