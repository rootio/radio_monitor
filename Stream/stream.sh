#!/bin/bash

arecord --device=plughw:1,0 --format S16_LE --rate 44100 -c2 | aplay --device=plughw:1,0 | lame -r -s 44.1 -m s -b 128 --preset cbr 192 - - |  ezstream -c ezstream.xml

