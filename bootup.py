import os
from crontab import CronTab
from pathlib import Path

#@reboot sleep 20 && python /home/pi/audiorecording.py

reqpath = str(Path().absolute()) +"/requirements.txt"
shpath = str(Path().absolute()) + "/startup.sh"
path = str(Path().absolute()) + "/audiorecording.py"

#cron.remove_all(comment='my comment')
#cron.remove(job)

with open("startup.sh",'w') as f:
    f.write("#!/bin/bash \ncd ~\nscreen -d -m python3 {} run".format(path))
    
cron = CronTab(user='pi')
cron.remove_all()
job = cron.new(command='sleep 20 && /usr/bin/screen -D -m {}'.format(shpath))
job.every_reboot()  

for item in cron:  
    print (item)
    
cron.write() 
job.enable()

os.system("chmod +x {}".format(shpath))
os.system("pip install -r {}".format(reqpath))