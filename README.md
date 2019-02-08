# radio_monitor
A simple embedded computer FM radio listener / analyzer to allow recording and analysis of FM radio stations, and internet retreival of this information. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/)

```bash
pip install pyaudio
pip install pydub
pip install python-crontab
*Other modules might be necessary
```

## Startup
Make sure you run bootup.py before starting using the script
This is to ensure the time is tracked in case the system's date is outdated

Simply run audiorecording.py to use it after

## Usage

```python
> help #commands
> channels #check channels available in the device
> channel #set the channel from the available devices

#The channel is already automaticaly set at startup

> duration #set duration for the recording time (seconds)

#The duration is set to record for 3600 sec by default i.e 1h

> storage #set the storage option of the saved recordings

#0 for flat and 1 for tree storage
#The storage option is by default selected to flat storage on the file the script is placed

> info #check the selected options
> save #save the selected options 

#Saving will ensure that the script will always record of a set of time and storage choosen

>exit #close program 

#Each command displayed has a help option included if necessary e.g > duration help
```

## License
[MIT](https://choosealicense.com/licenses/mit/)