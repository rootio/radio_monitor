import os
from crontab import CronTab
from pathlib import Path

reqpath = str(Path().absolute()) + "/requirements.txt"
shpath = str(Path().absolute()) + "/startup.sh"
path = str(Path().absolute()) + "/audiorecording.py"

os.system("sudo apt-get install python3-pyaudio")
os.system("sudo apt-get install python3-crontab")
os.system("sudo apt-get install screen")
os.system("pip3 install -r {}".format(reqpath))

with open("startup.sh",'w') as f:
    f.write("#!/bin/bash \ncd ~\nscreen -S goldenrecord -d -m python3 {} run".format(path))
    
cron = CronTab(user='pi')
cron.remove_all()
job = cron.new(command='sleep 20 && /usr/bin/screen -D -m {}'.format(shpath))
job.every_reboot()  

for item in cron:  
    print (item)
    
cron.write() 
job.enable()

os.system("chmod +x {}".format(shpath))
os.system("sudo sh startup.sh")
