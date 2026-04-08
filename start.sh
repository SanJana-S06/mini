#!/bin/sh
# Start Xvfb
Xvfb :99 -screen 0 1024x768x24 &
sleep 2
# Set display
export DISPLAY=:99
# Generate cookie
touch /root/.Xauthority
xauth add :99 . $(mcookie)
# Start the app
python server/app.py