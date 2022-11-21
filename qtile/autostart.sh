#!/usr/bin/env bash

picom --experimental-backends &
volumeicon &
nm-applet &
#~/.fehbg &
nitrogen --restore &
xrandr --output HDMI-1-1 --mode 1920x1080 --output eDP-1 --mode 1920x1080 --left-of HDMI-1-1
