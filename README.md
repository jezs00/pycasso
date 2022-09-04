# pycasso
System to send AI generated art to an E-Paper display through a Raspberry PI unit

## Acknowledgments

Inspiration for this project based on https://github.com/TomWhitwell/SlowMovie and the very helpful write-up available at https://debugger.medium.com/how-to-build-a-very-slow-movie-player-in-2020-c5745052e4e4 on setting up epaper to work with a Raspberry Pi unit.

Uses omni-epd so that this can work dynamically with many displays: https://github.com/robweber/omni-epd
Uses stability-sdk to interact with Stable Diffusion's API: https://github.com/Stability-AI/stability-sdk

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
