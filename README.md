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

### Get Raspberry Pi Ready
* Install Raspberry Pi OS from https://www.raspberrypi.com/software/operating-systems/ . When flashing SD card, ensure you set up your wireless details for easy access, otherwise you will have to follow configuration steps with the screen plugged in. Put the SD card into your Raspberry Pi unit

### (Optional) Plug in pijuice HAT
* If using, attach PiJuice HAT onto Raspberry Pi. See [pijuice documentation](https://github.com/PiSupply/PiJuice/blob/master/Software/README.md) for
more information. You can always do this later if you don't want to use PiJuice yet.

### Connect EPD to Pi
* CAREFULLY plug EPD into Raspberry Pi, or on top of pijuice HAT, following instructions from the vendor. pycasso implements omni-epd and should work with any EPD listed on this page: https://github.com/robweber/omni-epd/blob/main/README.md .
* Connect power directly to Raspberry Pi (or PiJuice unit) once done.

### Install pycasso
* SSH into the raspberry pi unit, or plug monitor and keyboard in.
* (Optional) Run `sudo apt-get update` and `sudo apt-get upgrade` to update system
* Run the following code to install pycasso in your home directory:
```
bash <(curl https://raw.githubusercontent.com/jezs00/pycasso/main/setup.sh)
```
* Take note of the proposed installation directory
* Select `Option 1` - Install/Upgrade pycasso
* Select "Yes" to enable service on boot if that is what you want to do _(it is probably what you want to do)_
* (Optional) If you want to use pijuice, select "Yes" to install PiJuice
* (Optional) Select `Option 5 - Apply GRPCIO Fix` _(There are issues with GLIBC on raspberry pi, and it was installed by the Stable Diffusion package. This fixes it up and does not appear to break Stable Diffusion. You'll probably have to do this.)_
  * If this does not work, try `Option 6 - Apply GRPCIO Update`. _(GRPCIO can be a tough cookie and acts differently on different operating systems, which makes this bit a little complicated)_
* Select `Option 7 - Set an API key or connect website`, enter your provider and enter your key. Currently supporting [openai](https://beta.openai.com/account/api-keys), [Stable Diffusion](https://beta.dreamstudio.ai/membership?tab=apiKeys). You can run this multiple times to add multiple providers or update your keys. **Please note that these providers are a paid service, and after any free credits expire, you will need to pay for more credits to maintain functionality.** _(You don't have to do this if you are loading external images, but to request images from an AI image provider, you'll need to define your API key here. By default, this will be stored in a plaintext file in the application folder. This is not ideal, but it is the best I have figured out until I can get GRPCIO playing nicely.)_
* (Optional) Select `Option 9 - Disable pijuice LEDs`. If you have a PiJuice unit, you can run this to disable the constantly flashing LED on the device to save precious battery.
* (Optional) Select `Option 10 - Install SMB and default shares`. This will set up a full access share in prompts and images folders, useful for easy management over the network but risky as it shares the folders with full permissions. Only do this on a trusted network. 

### Configure pycasso
* Make sure you are in your pycasso install directory.
* Run `nano .config` for all configuration options. There's a lot to play with here, and apart from file paths you should be able to play around and see what happens.
* The most important item of configuration is `[EPD]` - `type` . You should set this to the supported EPD you have plugged in, anything from [omni-epd's readme](https://github.com/robweber/omni-epd) should work, copy and paste the appropriate EPD string and paste it here instead of omni_epd.mock. Leaving type as omni_epd.mock will generate a png file in this folder instead of updating the display.
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
* If you have run through the installation and pycasso is working, it will run on startup. Normal behaviour is to run once and close, if you have an always-on system, you may wish to disable the service and just run pycasso or start the service through cron.
* With a PiJuice, you can configure `shutdown_on_battery` to automatically shut down and remove power to the board when pycasso is done, to complete a headless fully battery driven process. Be a little careful with this as to save battery, it prefers to shut down above all else, even on exception. If you experience a program error you will only have `wait_to_run` (default 30) seconds to connect to the pi and disable the service to fix.
* Play around a bit with the `.config` options so that everything on the screen looks good to you and works for your implementation. There is a description of all configuration items in the file. While experimenting, I recommend setting the mode to only fetch images from historic backlog using `historic_amount`, so that you aren't spending credits on your API while setting it up.
* Configure your prompts to send to providers using /prompts/artists.txt, /prompts/subjects.txt and /prompts/prompts.txt
  * Review the markup of the example prompts to learn how to apply randomisation for interesting effect in your prompt
  * Have a play around with the prompts and see what works for you. See [Bracket wildcards](#bracket-wildcards) and [Prompt Blocks](#prompt-blocks) for more information.

### Administration
* Access to the prompt generation files, configuration, and saved images may be complicated through your raspberry pi unit. I recommend setting up an SMB share for easy access to these folders. Feature request to set this up automatically is tracked [here](https://github.com/jezs00/pycasso/issues/19).
* If you have set `shutdown_on_battery` to true, you should be able to plug your PiJuice into power to ensure it stays on when you start it.
* If a disaster occurs, and you have `shutdown_on_battery` and `shutdown_on_exception` both set to True and you cannot keep the device on long enough to log in, you might need to unplug the SD card and try to fix the config. If this option is not available to you, it's possible you might need to flash it and start from scratch. A possible solution to these issues while maintaining a priority on extending battery life is being tracked [here](https://github.com/jezs00/pycasso/issues/20).

### Bracket Wildcards
To enhance dynamic prompt generation within pycasso, many text files and strings in pycasso are parsed to replace wildcard text. This allows more flexibility when defining prompts.

In the past, the three types of brackets used are:
1. ()
2. []
3. {}

These can be added to, removed, or customised in `.config`. They are included to keep functionality by default with any old text parsers, however there is no reason to use multiple brackets anymore. It is suggested to just use ().

Different options are separated by a pipe, for example `(Option 1|Option 2|(Option (3|4|5|6)|Option 7))`. The parser will first look for the lowest level of brackets, choose only one random option of the text, and then proceed to the next levels. Unless otherwise specified, each option has an equal chance of being chosen from each bracket pair. This means with nested brackets, you should consider the way the parsing works when thinking about the likelihood of a certain item of text occurring. For example, `A (Good|(B|R)ad) Dog` could return `A Good Dog` `A Bad Dog` or `A Rad Dog`. The option will be picked randomly between each bracket pair, so you have 50% chance of `A Good Dog`, 25% chance of `A Bad Dog` and 25% chance of `A Rad Dog`.

At the start of any segment, you can also provide a weighting for a particular option. For example `(20:Option A|Option B|0:Option C)` should provide `Option A` about 20 times more often than `Option B`. `Option C` would never appear. These weightings can also be used at the start of every line in one of the prompt-building text files to specify the likelihood of that line being chosen.

Have a play around with the strings and see what works for you. You can leave the EPD in test mode with no provider modes selected, and the test display will show you what subject it would have fetched. 

Here are a few more examples of how one may use these to make simple prompts more complex:

`A (|Happy|Sad) (Dog|Cat|Bird)` could result in:
* `A Dog`, `A Happy Dog`, `A Sad Dog`, `A Cat`, `A Happy Cat`, `A Sad Cat`, `A Cat`, `A Happy Bird` or `A Sad Bird`. All options have the same probability of occurring.

`A (Dog|Cat) (|(Carrying|Stealing) A(n Apple| Banana))` could result in:
* **1/4** of the time `A Dog`, **1/4** of the time `A Cat`, **1/16** of the time `A Dog Carrying An Apple`, **1/16** of the time `A Dog Carrying A Banana`, **1/16** of the time `A Dog Stealing An Apple`, **1/16** of the time `A Dog Stealing A Banana`, **1/16** of the time `A Cat Carrying An Apple`, **1/16** of the time `A Cat Stealing An Apple`, **1/16** of the time `A Cat Stealing An Apple` or **1/16** of the time `A Cat Stealing A Banana`

`A(5: Friendly|2:n Uncommon| Rare) (3:Dog|Cat)` could result in:
* **15/32** of the time `A Friendly Dog`, **3/16** of the time `An Uncommon Dog`, **3/32** of the time `A Rare Dog`, **5/32** of the time `A Friendly Cat`, **1/16** of the time `An Uncommon Cat` or **1/32** of the time `A Rare Cat`

### Prompt Blocks
pycasso now supports "Prompt Blocks" when enabled in config. These allow far more dynamic prompts to be used. By default, this uses the <> characters and specifies a part of the text to process. Detection and processing is performed inside-out, so results of process blocks can be nested and passed as arguments or text to other blocks. Blocks also work with wildcards as defined above, allowing for a great amount of flexibility and diversity in generation options.

* For example, `<llm;<quote>> in the style of Lichtenstein` attempts to load a quote from zenquotes, then pass it to an llm to turn the text into something to be consumed by one of the image generation providers
* All prompt blocks should return a blank string on failures, so your prompt will still attempt to build itself even if one prompt block fails.

Some prompt blocks accept arguments. By default, the seperator between arguments is ';', however this can be modified in the configuration.
* For example `<file;path/to/file>` will load a line from the file located at `path/to/file`

As the generated text can be unpredictable and long, we can also specify what we want the subject to be if enabled in config and we are displaying text on the screen. By default, we use {} characters to do this:
* With the minor modification of `<llm;{<quote>}> in the style of Lichtenstein` we can now ensure that while we still use enriched text by the LLM to request the image, only the quote is displaying as the text on our screen.

Detection and processing of blocks is recursive and all-inclusive. This means prompt blocks located in files, config, and generated by other methods will all be processed. The best way to learn how to use this is to play around and see what is possible. 

#### Block Types

* `<file>`: The file block loads one line of text from a file. Text within the file is also processed with wildcards as defined above. The text is also parsed for process blocks. Requires path to file to be provided as an argument.
  * Example usage: `<file;path/to/file>` - Loads a line from the file `path/to/file`
* `<llm>`: The llm block requests an llm to enhance or respond to a provided prompt. Currently openai/chatgpt is the only api available. Instructions for the ai to use to process the text are defined using the variable `llm_system_prompt` available in .config 
  * Example usage: `<llm;requested prompt>` - Returns the result of an LLM being provided the text `requested prompt` 
* `<rss>`: The rss block pulls an rss feed from a provided link, and returns text from the feed. Requires path/url to rss feed to be provided as an argument. Optional arguments can be provided to define the tag (defaults to `title`, which works for most news rss providers) to export from the items, and to define the index of items to export (defaults to `0` for most recent item).
  * Example usage: `<rss;https://testnews.notarealwebsite/feed>` - Returns the title of the most recent news item provided
  * `<rss;https://testnews.notarealwebsite/feed;description>` - Returns the description of the most recent news item provided
  * `<rss;https://testnews.notarealwebsite/feed;title;2>` - Returns the title of the 3rd most recent news item provided
* `<quote>`: The quote block provides an 'inspirational' quote from zenquotes. Best utilised with an llm to massage the quote into the artwork
  * Example usage: `<quote>` - Returns a quote in its entirety

#### Examples

* `<llm;(<file;path/to/file>|<quote>)>` - Sends either a line from the file `path/to/file` or a quote from zenquotes to the llm, and then returns the response from the llm
* `<rss;https://testnews.notarealwebsite/feed> in the style of <file;path/to/file>` - Provides a prompt that has a news item modified by an artist or theme provided in `path/to/file`

## Configuration
You can run `nano .config` in the pycasso install folder to configure the way pycasso runs. There are a lot of options to configure your experience, and it is highly recommended to play around with these options to find the settings that work best for your setup. If at any time you wish to roll back to the default configuration you can find it is `/examples/.config-example`, or you can delete .config and running pycasso will restore the defaults automatically. If you are running pycasso frequently to see what changes your updates make, it is recommended to either use the test mode by setting all providers to 0, or using external/generated modes so that you are not being charged by your provider for each time you run the program. Below you will find a full explanation of all configuration sections and items.

### File
Settings related to file operations within pycasso

* `save_image`: A boolean flag that instructs pycasso whether to save images retrieved from providers or not. If 'True', pycasso will always save images retrieved in a defined location. If 'False' pycasso will only display the image on the EPD, once the EPD is updated again this image will be lost. `(Boolean)`
* `save_date`: A boolean flag that instructs pycasso whether to append a datetime at the start of the saved filename. `(Boolean)`
* `external_image_location`: A file path relative to the pycasso working directory to load external images from, when using **external** mode. `(String)`
* `generated_image_location`: A file path relative to the pycasso working directory to save generated images to when using a provider, and load them from when using **generated** mode. `(String)`
* `image_format`: The file type to look for when loading images from external or generated image folders. Most of the time it will be "png". `(String)`
* `font_file`: A file path relative to the pycasso working directory to load a font file from. This supports drawing text on the EPD. `(String)`
* `subjects_file`: A file path relative to the pycasso working directory to load 'subjects' from when using prompt mode 1. `(String)`
* `artists_file`: A file path relative to the pycasso working directory to load 'artists' from when using prompt mode 1. `(String)`
* `subjects_file`: A file path relative to the pycasso working directory to load 'prompts' from when using prompt mode 2. `(String)`
* `resize_external`: A boolean flag that instructs pycasso whether to resize external images. If 'True', pycasso will resize images provided to it so that the whole image will fit in the EPD. If 'False', pycasso will fill the whole screen with the image by resizing to a smaller extent, and then cropping. `(Boolean)`
* `file_name_max_length`: The maximum length in characters a filename can be. `(Integer)`

### EPD
These settings are consumed by omni-epd to customise the EPD information. See [omni-epd](https://github.com/robweber/omni-epd) for supported displays for more information on omni-epd options

* `type`: The type of EPD display being used. See [omni-epd](https://github.com/robweber/omni-epd#displays-implemented) for supported displays and their names. `(String)`
* `mode`: The color mode to run the EPD with. See [omni-epd](https://github.com/robweber/omni-epd#displays-implemented) for supported modes of each display. `(String)`
* `palette_filter`: By default not required and commented out. Uncomment and configure based on information provided [here](https://github.com/robweber/omni-epd#virtualepd-object) if you wish to customise the palette. Required for dithering. `(Tuple)`

### Display
These settings are consumed by omni-epd to customise the display on the EPD. See [omni-epd](https://github.com/robweber/omni-epd) for more information on these options.

* `rotate`: Rotation of the image in degrees. You probably don't need to use this, use the other rotate option in Generation instead. `(Integer)`
* `flip_horizontal`: A boolean flag that instructs the EPD to flip the image horizontally or not `(Boolean)`
* `flip_vertical`: A boolean flag that instructs the EPD to flip the image vertically or not `(Boolean)`
* `dither`: By default commented out. Uncomment to set a dithering mode to use. See [the omni-epd wiki](https://github.com/robweber/omni-epd/wiki/Image-Dithering-Options) for supported modes and more information. `(String)`
* `dither_strength`: By default commented out. Uncomment if using `dither`. Sets the strength of the dithering algorithm. See [the omni-epd wiki](https://github.com/robweber/omni-epd/wiki/Image-Dithering-Options) for more information. `(Float)`
* `dither_serpentine`: By default commented out. Uncomment if using `dither`. A boolean flag that instructs the dithering algorithm to use serpentine dithering or not. See [the omni-epd wiki](https://github.com/robweber/omni-epd/wiki/Image-Dithering-Options) for more information. `(Boolean)`

### Image Enhancements
These settings are consumed by omni-epd to customise the display on the EPD. See [omni-epd](https://github.com/robweber/omni-epd) for more information on these options.

* `contrast`: Sets contrast amount for EPD. 1 is normal. `(Integer)`
* `brightness`: Sets brightness amount for EPD. 1 is normal. `(Integer)`
* `sharpness`: Sets sharpness amount for EPD. 1 is normal. `(Integer)`

### Prompt
Settings related to creation of prompts for submission and requests from AI art providers

* `mode`: The mode to use in prompt generation. `(Integer)` This currently supports 3 different types of modes:
  * `1` -  (`preamble` - **subjects.txt** - `connector` - **artists.txt** - `postscript`)
  * `2` -  (`preamble` - **prompts.txt** - `postscript`)
  * `0` -  Any of the above (randomly chooses one of the above options)
* `preamble`: Text that fills in the `preamble` part of the prompt construction above. [Bracket wildcards](#bracket-wildcards) and [Prompt Blocks](#prompt-blocks) supported.`(String)`
* `connector`: Text that fills in the `connector` part of the prompt construction above. [Bracket wildcards](#bracket-wildcards) and [Prompt Blocks](#prompt-blocks) supported.`(String)`
* `postscript`: Text that fills in the `postscript` part of the prompt construction above. [Bracket wildcards](#bracket-wildcards) and [Prompt Blocks](#prompt-blocks) supported.`(String)`

### Text
Settings related to parsing text of filenames and strings, and text display on the EPD

* `add_text`: A boolean flag that instructs pycasso whether to display a textbox on the EPD or not. `(Boolean)`
* `use_blocks`: A boolean flag that instructs pycasso whether to interpret certain strings using [Prompt Blocks](#prompt-blocks) or not. `(Boolean)`
* `specify_subject`: A boolean flag that instructs pycasso whether to allow specifying of subjects or not. `(Boolean)`
* `parse_file_text`: A boolean flag that instructs pycasso whether to parse filenames in external image mode or not. `(Boolean)`
* `preamble_regex`: Normal regex to find the split point between the preamble and the main text in external image names. `(String)`
* `artist_regex`: Normal regex to find the split point between the subject and artist in external image names. `(String)`
* `remove_text`: A list of strings to find and completely remove from any file names to parse into pycasso. `(List)`
* `parse_random_text`: A boolean flag that instructs pycasso whether to interpret certain strings using [bracket wildcards](#bracket-wildcards) or not. `(Boolean)`
* `parse_brackets`: A list of bracket pairs in order of the highest to the lowest level in hierarchy. `(List)`
* `block_brackets`: A string with 2 bracket pairs to be used to specify blocks to use in [Prompt Blocks](#prompt-blocks). Recommend using uncommon brackets. `(String)`
* `block_seperator`: A string with 1 character to be used to separate arguments in blocks from [Prompt Blocks](#prompt-blocks). Recommend using an uncommon character. `(String)`
* `subject_brackets`: A string with 2 bracket pairs to be used to specify the subject when using [Prompt Blocks](#prompt-blocks). Recommend using uncommon brackets. `(String)`
* `box_to_floor`: A boolean flag that instructs pycasso whether to draw the text box all the way to the bottom of the image instead of just appearing around the text. `(Boolean)`
* `box_to_edge`: A boolean flag that instructs pycasso whether to draw the text box all the way to the edges of the image instead of just appearing around the text. `(Boolean)`
* `artist_loc`: Distance in pixels of the artist text away from the bottom of the image. `(Integer)`
* `artist_size`: Font size of the artist text. `(Integer)`
* `title_loc`: Distance in pixels of the title text away from the bottom of the image. `(Integer)`
* `title_size`: Font size of the title text. `(Integer)`
* `padding`: Padding of the text box containing title and artist text. `(Integer)`
* `opacity`: Opacity of the text box. 0 for fully transparent and 255 for fully opaque. `(Integer)`
* `override_text`: A boolean flag to indicate whether to override final text with other text from a file `(Boolean)`
* `override_path`: A file path relative to the pycasso working directory to load the override text from when override_text is enabled `(String)`

### Icon
Settings related to status icons to display on EPD

* `icon_color`: Color to show icon in. Set to `auto` to automatically detect white or black depending on shade of background `(String)` 
* `icon_padding`: Padding from the top left corner in pixels to place the icon `(Integer)`
* `icon_corner`: Which corner to place the icons in. Can be `nw`, `ne`, `sw` or `se`. `(String)`
* `icon_size`: Size of the status icon in pixels `(Integer)`
* `icon_width`: The width of the line of the status icon in pixels (currently unused due to new icon system) `(Integer)`
* `icon_gap`: Gap in pixels in between individual icons `(Integer)`
* `icon_opacity`: Opacity of the status icon. 0 for fully transparent and 255 for fully opaque. `(Integer)`
* `icon_path`: A file path relative to the pycasso working directory to find the icons in. `(String)`
* `show_battery_icon`: A boolean flag that instructs pycasso to show a battery status icon. `(Boolean)` 
* `show_provider_icon`: A boolean flag that instructs pycasso to show an icon based on provider used, and any provider failure. `(Boolean)` 
* `show_status_icon`: A boolean flag that instructs pycasso to show an icon on exception. `(Boolean)`

### Logging
Settings related to error and information logging from pycasso.
* `log_file`: A file path relative to the pycasso working directory to save log file `(String)`
* `log_level`: Minimum logging level to save to log file. Possible options - CRITICAL:50, ERROR:40, WARNING:30, INFO:20, DEBUG:10, NOTSET:0 `(Integer)`

### Providers
Settings related to image providers.

* The following items are integers providing the 'comparative chance' they will be chosen. This means you could choose multiple provider modes and pycasso will randomly choose one of them. The higher integer gives a higher chance of being picked. For example, `external_amount = 0`, `historic_amount = 1` and `stability_amount = 2` would result in **External** images never appearing, and approximately 1 **Historic** image appearing for every 2 **Stable Diffusion** images. If all options are set to 0, pycasso will either exit or run its test mode depending on the value of `test_enabled`.
  * `external_amount`: The comparative chance of pycasso running External mode (loading an image from the `external_image_location` folder). `(Integer)`
  * `historic_amount`: The comparative chance of pycasso running Historic mode (loading an image from the `generated_image_location` folder). `(Integer)`
  * `stability_amount`: The comparative chance of pycasso running Stable Diffusion mode (loading an image online from Stable Diffusion). `(Integer)`
  * `dalle_amount`: The comparative chance of pycasso running DALLE mode (loading an image online from DALLE). `(Integer)`
  * `automatic_amount`: The comparative chance of pycasso running Automatic1111 Stable Diffusion WebUI mode (loading an image from a valid Automatic1111 API). `(Integer)`
* `use_keychain`: A boolean flag that instructs pycasso whether to use keychain to manage keys. When set to false will just look for .creds file with credentials in it. This may or may not work depending on your board. See [grpcio issues](https://github.com/jezs00/pycasso/issues/1) for more information. `(Boolean)`
* `credential_path`: A file path relative to the pycasso working directory to find API credentials. `(String)`
* `test_enabled`: A boolean flag that instructs pycasso to run a test mode when all other providers are set to 0. `(Boolean)`
* `stable_host`: A string that provides the API location to send the request to for Stable Diffusion online. `(String)`
* `automatic_host`: If using `automatic` mode, this is the IP address or host of the Automatic1111 WebUI API. `(String)`
* `automatic_port`: If using `automatic` mode, this is the port to use for the Automatic1111 WebUI API. `(Integer)`
* `provider_fallback`: A boolean flag that instructs pycasso to fall back to another random non-zero provider if originally chosen provider fails. `(Boolean)`
* `llm_model`: The model to use for the llm block `(String)`
* `llm_temperature`: Controls randomness in the output (0.0-1.0) `(Float)`
* `llm_max_tokens`: Maximum number of tokens in the response `(Integer)`
* `llm_system_prompt`: Prompt to encourage the LLM to do what you want it to do `(String)`

### Generation
Settings related to generation of images with AI image providers

* `image_rotate`: Rotation of the image PRIOR to sending to providers. This way you can get an image that fits well in portrait or landscape as per your preference. `(Integer)`
* `infill`: A boolean flag that instructs pycasso to request an image to be infilled again if original image does not fill out the whole frame. `(Boolean)`
* `infill_percent`: If infill is set to true, this will make the original image request smaller by this percentage, and then infill the rest of the image to fit the frame. `(Integer)`

### PiJuice
Settings related to PiJuice HAT configuration.

* `use_pijuice`: A boolean flag that instructs the run script whether to use PiJuice classes. `(Boolean)`
* `shutdown_on_battery`: A boolean flag that instructs the run script whether to shut down the raspberry pi if PiJuice is running on battery (not plugged in to power). `(Boolean)`
* `shutdown_on_exception`: A boolean flag that instructs the run script whether to shut down if program encounters an exception. Used to stop battery running down on error. **WARNING: Worst case scenario this could result in having to flash your device, if pycasso keeps restarting after failures you may not be able to SSH in even after a wait time**. `(Boolean)`
* `wait_to_run`: Time to wait in seconds before running pycasso. Can help in ensuring PiJuice class is ready, and gives a buffer to SSH into device if encountering issues. `(Integer)`
* `charge_display`: Battery percentage that pycasso should start showing low battery symbol. `(Integer)`

### Post
Settings related to posting and sharing pycasso output on the web. Use set_keys.py to set up.
* `post_connector`: A string to put between subject and artist if posting in this mode. `(String)`
* `post_to_mastodon`: A boolean flag that instructs pycasso to attempt to post image to Mastodon. `(Boolean)`
* `mastodon_app_name`: The app name to associate with your account. `(String)`
* `mastodon_base_url`: The url to the account's mastodon instance `(String)`
* `mastodon_client_cred_path`: A file path relative to the pycasso working directory to mastodon's client secret `(String)`
* `mastodon_user_cred_path`: A file path relative to the pycasso working directory to mastodon's user secret  `(String)`

### Debug
The following settings are only relevant for development. Only use them if you know what you're doing.
* `test_epd_width`: Width in pixels to set the mock EPD to. Mostly for testing purposes. `(Integer)`
* `test_epd_height`: Height in pixels to set the mock EPD to. Mostly for testing purposes. `(Integer)`

## Troubleshooting

### There is a symbol on the top left of the screen
By default, pycasso puts a faint symbol on the top left of the EPD to inform of system events. By default, these are:
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

### Module I2C Missing
I have found this might cause issues with PiJuice. This is possibly due to running a lite version of the operating system. I found success by:
* Updating the kernel with `sudo rpi-update`
* Rebooting
* Running `sudo raspi-config`
 * Selecting `Interface Options -> I2C -> Yes`

### Log an issue
If you're experiencing a bug or issue, or have a feature request, please visit the [Issues](https://github.com/jezs00/pycasso/issues) page to let us know. Recommend including the relevant information provided in `pycasso.log` and your current `.config`
