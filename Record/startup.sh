#!/bin/bash
cd ~
screen -S goldenrecord -d -m python3 /home/pi/audiorecording.py run
