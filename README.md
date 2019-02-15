# radio_monitor
A simple embedded computer FM radio listener / analyzer to allow recording and analysis of FM radio stations, and internet retreival of this information. 

## Installation

```bash
Run bootup.py if you are using this for the first time or in a fresh OS!

#Manually install requirements if needed:
Use the package manager [pip](https://pip.pypa.io/en/stable/)
pip install -r requirements.txt
```

## Startup

Simply run audiorecording.py to use 

To bypass the menu add run when calling the script:
>python3 audiorecording.py run


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

## Project 
[RootIO](http://rootio.org/)