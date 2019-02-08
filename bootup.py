from crontab import CronTab
from pathlib import Path

#@reboot sleep 20 && python /home/pi/audiorecording.py

path = str(Path().absolute()) + "/timerequest.py"

#cron.remove_all(comment='my comment')
#cron.remove(job)

cron = CronTab(user='pi')
cron.remove_all()
job = cron.new(command='sleep 30 && export DISPLAY=:0.0 && python {}'.format(path))
job.every_reboot()  

for item in cron:  
    print (item)
    
cron.write() 
job.enable()