# pycasso
System to send AI generated art to an E-Paper display through a Raspberry PI unit

## Acknowledgments

Inspiration for this project based on https://github.com/TomWhitwell/SlowMovie and the very helpful write-up available at https://debugger.medium.com/how-to-build-a-very-slow-movie-player-in-2020-c5745052e4e4 on setting up epaper to work with a Raspberry Pi unit.

Uses omni-epd so that this can work dynamically with many displays: https://github.com/robweber/omni-epd

Uses stability-sdk to interact with Stable Diffusion's API: https://github.com/Stability-AI/stability-sdk

## Setup

### Turn on SPI
* Run`sudo raspi-config`
* Navigate to Interface Options > SPI
* Select <Finish> to exit. Reboot if prompted.


### Install prerequisites
```
python3 pip install git+https://github.com/Stability-AI/stability-sdk.git
python3 pip install git+https://github.com/robweber/omni-epd.git@v0.3.1#egg=omni-epd
python3 pip install https://github.com/openai/openai-python.git
```


### Run on startup
Add the following command to rc.local:
(rc.local works best as far as I can tell from testing)

* If using dbus for key management: `sudo dbus-run-session -- bash <Path to pycasso>/run.sh`
* Otherwise: `sudo python3 <Path to pycasso>/pijuice_script.py`

### Configure
* `nano .config` for all configuration options

### Configure pijuice
* See [pijuice documentation](https://github.com/PiSupply/PiJuice/blob/master/Software/README.md) for
more information. You can set the pijuice to wake up every day at a certain time.
Recommend turning off battery LED permanently to avoid draining battery.

## Troubleshooting

### GLIBC_2.33 not found
I have experienced this error even with the most recent release of raspbian.
Following [this](https://stackoverflow.com/questions/71054519/glibc-2-33-not-found-in-raspberry-pi-python) appears to work:
```
sudo pip3 uninstall grpcio 
sudo pip3 uninstall grpcio-status 
sudo pip3 install grpcio==1.44.0 --no-binary=grpcio
sudo pip3 install grpcio-tools==1.44.0 --no-binary=grpcio-tools
```
This is only required until a better solution is found
