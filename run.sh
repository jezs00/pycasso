#! usr/bin/bash
echo -n 'db' | gnome-keyring-daemon --unlock
python3 pycasso.py
