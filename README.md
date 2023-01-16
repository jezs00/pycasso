# pycasso
System to send AI generated art to an E-Paper display through a Raspberry PI unit

An article has been published on pycasso's development [here](https://jezs00.medium.com/pycasso-how-to-build-a-picture-frame-to-show-you-random-ai-art-every-day-44a1d3d78237).

| ![Pycasso At Home](https://i.imgur.com/GxhmODU.jpg) | 
|:--:| 
| *Yee-ha.* |

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
* Select `Option 5 - API Key`, enter your provider and enter your key. Currently supporting [openai](https://beta.openai.com/account/api-keys) and [Stable Diffusion](https://beta.dreamstudio.ai/membership?tab=apiKeys). You can run this multiple times to add multiple providers or update your keys. _(You don't have to do this if you are loading external images, but to request images from an AI image provider, you'll need to define your API key here. By default this will be stored in a plaintext file in the application folder. This is not ideal but it is the best I have figured out until I can get GRPCIO playing nicely.)_
* OPTIONAL: Select `Option 6 - Disable pijuice LEDs`. IF you have a PiJuice unit, you can run this to disable the constantly flashing LED on the device to save precious battery.

### Configure pycasso
* Make sure you are in your pycasso install directory.
* Run `nano .config` for all configuration options. There's a lot to play with here, and apart from file paths you should be able to play around and see what happens.
* The most important item of configuration is `[EPD]` - `type` . You should set this to the supported EPD you have plugged in, anything from [omni-epd's readme](https://github.com/robweber/omni-epd) should work, copy paste the appropriate EPD string and paste it here instead of omni_epd.mock. Leaving type as omni_epd.mock will generate a png file in this folder instead of updating the display.
* run `python3 examples/review_screen.py` and see if it works on your screen. _(If your screen is not displaying an image there's most likely a problem with your EPD, you can also check pycasso.log to troubleshoot)_

### Configure PiJuice
* Run `pijuice_cli` to configure your PiJuice unit.
* See [PiJuice documentation](https://github.com/PiSupply/PiJuice/blob/master/Software/README.md) for
more information. My preferred configuration is to set a wakeup timer to start at a preferred time daily, but you can set this as you see fit.
* You can configure the buttons on the PiJuice to perform different functions. I recommend leaving the first switch as power on device, as this is very useful for cycling the image or for turning the device on while powered to administer.


| ![PiJuice CLI Menu](https://i.imgur.com/npZJSTK.png) | 
|:--:| 
| *PiJuice CLI Menu* |


| ![PiJuice CLI Wakeup](https://i.imgur.com/w6i53wM.png) | 
|:--:| 
| PiJuice CLI Wakeup Configuration |

### Run pycasso
* Run `sudo systemctl restart pycasso` and see if it worked!

### Customise pycasso
* If you have run through the install and pycasso is working, it will run on startup. Normal behaviour is to run once and close, if you have an always-on system, you may wish to disable the service and just run pycasso or start the service through cron.
* With a PiJuice, you can configure `shutdown_on_battery` to automatically shut down and remove power to the board when pycasso is done, to complete a headless fully battery driven process. Be a little careful with this as to save battery, it prefers to shutdown above all else, even on exception. If you experience a program error you will only have `wait_to_run` (default 30) seconds to connect to the pi and disable the service to fix.
* Play around a bit with the `.config` options so that everything on the screen looks good to you and works for your implementation. There is a description of all configuration items in the file. While experimenting, I recommend setting the mode to only fetch images from historic backlog using `historic_amount`, so that you aren't spending credits on your API while setting it up.
* Configure your prompts to send to providers using /prompts/artists.txt, /prompts/subjects.txt and /prompts/prompts.txt
  * Review the markup of the example prompts to learn how to apply randomisation for interesting effect in your prompt
  * You can use hierarchical brackets to randomise elements in the prompt
    * EG `A (Good|[B|R]ad) Dog` could return `A Good Dog` `A Bad Dog` or `A Rad Dog`. Option picked randomly between each bracket pair, so you have 50% chance of `A Good Dog`, 25% chance of `A Bad Dog` and 25% chance of `A Rad Dog`
  * You can add weights to entire lines or brackets to increase their likelihood. Integers only.
    * EG You could expect `A (4:Good|Bad|0:Happy) Dog` should return `A Good Dog` around 4 times for every `A Bad Dog`. `A Happy Dog` would never appear.
  * Have a play around with the prompts and see what works for you

### Administration
* Access to the prompt generation files, configuration, and saved images may be complicated through your raspberry pi unit. I recommend setting up a SMB share for easy access to these folders. Feature request to set this up automatically is tracked [here](https://github.com/jezs00/pycasso/issues/19).
* If you have set `shutdown_on_battery` to true, you should be able to plug your PiJuice into power to ensure it stays on when you start it.
* If a disaster occurs and you have `shutdown_on_battery` and `shutdown_on_exception` both set to True and you cannot keep the device on long enough to log in, you might need to unplug the SD card and try to fix the config. If this option is not available to you, it's possible you might need to flash it and start from scratch. A possible solution to these issues while maintaining a priority on extending battery life is being tracked [here](https://github.com/jezs00/pycasso/issues/20).

## Troubleshooting

### There is a symbol on the top left of the screen
By default, pycasso puts a faint symbol on the top left of the EPD to inform of system events. By default these are:
* Square for low battery _(low battery warning level configurable in `.config`, default 15%)_
* Cross for exception _(likely PiJuice failing to load if you are using it, try a longer `wait_to_run`)_ . If you have anything odd in your `pycasso.log` file you can post it [here](https://github.com/jezs00/pycasso/issues).

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

### Log an issue
If you're experiencing a bug or issue, or have a feature request, please visit the [Issues](https://github.com/jezs00/pycasso/issues) page to let us know. Recommend including the relevant information provided in `pycasso.log` and your current `.config`
