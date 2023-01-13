# pycasso
System to send AI generated art to an E-Paper display through a Raspberry PI unit

![Pycasso On The Wall](https://i.imgur.com/AUPlb3y.jpg)

## Acknowledgments

Inspiration for this project based on Tom Whitwell's [SlowMovie](https://github.com/TomWhitwell/SlowMovie) and the very helpful write-up available at https://debugger.medium.com/how-to-build-a-very-slow-movie-player-in-2020-c5745052e4e4 on setting up epaper to work with a Raspberry Pi unit. I also liberally reused a lot of the install.sh script from this project because of the similarities and because it's pretty good. I would also like to acknowledge [robweber](https://github.com/robweber) who not only created [omni-epd](https://github.com/robweber/omni-epd) which I implemented so that this can work dynamically with many displays, but also provided me with a lot of good code examples that I referred back to often to try to ensure I was following best practises.

Uses [stability-sdk](https://github.com/Stability-AI/stability-sdk) to interact with Stable Diffusion's API.

Uses [openai-python](https://github.com/openai/openai-python) to interact with DALL-E's API.

## Setup

### Get Raspberri Pi Ready
* Install Raspberry Pi OS from https://www.raspberrypi.com/software/operating-systems/ . When flashing SD card, ensure you set up your wireless details for easy access, otherwise you will have to follow configuration steps with the screen plugged in. Put the SD card into your Raspberry Pi unit

### OPTIONAL: Plug in pijuice HAT
* If using, attach PiJuice HAT onto Raspberry Pi. See [pijuice documentation](https://github.com/PiSupply/PiJuice/blob/master/Software/README.md) for
more information. You can always do this later if you don't want to use PiJuice yet.

### Connect EPD to Pi
* CAREFULLY plug EPD into Raspberry Pi, or on top of pijuice HAT, following instructions from the vendor. pycasso implements omni-epd and should work with any EPD listed on this page: https://github.com/robweber/omni-epd/blob/main/README.md .
* Connect power directly to Raspberry Pi (or PiJuice unit) once done.

### Install pycasso
* SSH into the raspberry pi unit, or plug monitor and keyboard in.
* Run the following code to install pycasso in your home directory:
```
bash <(curl https://raw.githubusercontent.com/jezs00/pycasso/main/setup.sh)
```
* Take note of the proposed install directory
* Select `Option 1` - Install/Upgrade pycasso
* Select "Yes" to enable service on boot if that is what you want to do _(it is probably what you want to do)_
* OPTIONAL: If you want to use pijuice, select "Yes" to install PiJuice
* OPTIONAL: Select `Option 4` - Fix GRPCIO _(There are issues with GLIBC on raspberry pi and it was installed by the Stable Diffusion package. This fixes it up and does not appear to break Stable Diffusion. You'll probably have to do this.)_
* OPTIONAL: Select `Option 5 - API Key`, enter your provider and enter your key. You can run this multiple times to add multiple providers or update your keys. _(You don't have to do this if you are loading external images, but to request images from an AI image provider, you'll need to define your API key here. By default this will be stored in a plaintext file in the application folder. This is not ideal but it is the best I have figured out until I can get GRPCIO playing nicely.)_
* OPTIONAL: Select `Option 6 - Disable pijuice LEDs`. IF you have a PiJuice unit, you can run this to disable the constantly flashing LED on the device to save precious battery.

### Configure pycasso
* Make sure you are in your pycasso install directory.
* Run `nano .config` for all configuration options. There's a lot to play with here, and apart from file paths you should be able to play around and see what happens.
* The most important item of configuration is `[EPD]` - `type` . You should set this to the supported EPD you have plugged in, anything from [omni-epd's readme](https://github.com/robweber/omni-epd) should work, copy paste the appropriate EPD string and paste it here instead of omni_epd.mock. Leaving type as omni_epd.mock will generate a png file in this folder instead of updating the display.
* run `python3 examples/review_screen.py` and see if it works on your screen. _(If your screen is not displaying an image there's most likely a problem with your EPD, you can also check pycasso.log to troubleshoot)_

### Configure PiJuice
* Run `pijuice_cli` or `pijuice_gui` to configure your PiJuice unit.
* See [PiJuice documentation](https://github.com/PiSupply/PiJuice/blob/master/Software/README.md) for
more information. My preferred configuration is to set a wakeup timer to start at a preferred time daily, but you can set this as you see fit.

### Run pycasso
* Run `sudo systemctl restart pycasso` and see if it worked!

## Troubleshooting

### GLIBC_2.33 not found
I have experienced this error even with the most recent release of raspbian.
Following [this](https://stackoverflow.com/questions/71054519/glibc-2-33-not-found-in-raspberry-pi-python) appeared to work, however I haven't had any luck for a while. It might work for you:
```
sudo pip3 uninstall grpcio 
sudo pip3 uninstall grpcio-status 
sudo pip3 install grpcio==1.44.0 --no-binary=grpcio
sudo pip3 install grpcio-tools==1.44.0 --no-binary=grpcio-tools
```
If you can't store your credentials in keyring, you'll have to set the `use_keyring` option in `.config` to False, and provide your credentials using `setup.sh` option 5 or `set_keys.py`
