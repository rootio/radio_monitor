#!/bin/bash
if nc -zw1 google.com 443; then
  echo "IPv4 is up!"
else
  echo "IPv4 is down"
  sleep 10
fi
arecord --device=plughw:1,0 --format S16_LE --rate 44100 -c2 |  tee >(aplay --device=plughw:1,0) | lame -r -s 44.1 -m s -b 128 --preset cbr 192 - - |  ezstream -c ezstream.xml