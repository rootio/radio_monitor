import os
from pathlib import Path

#Paths used:

mypath = str(Path().absolute())

#Adding folders
os.system("sudo mkdir -p {}/Record".format(mypath))
os.system("sudo mkdir -p {}/Stream".format(mypath))

#Paths
reqpath = mypath + "/requirements.txt" #Install from requirements.txt
path = mypath + "/audiorecording.py" #Script path
#startupSh = mypath + "/startup.sh" #Screen startup (crontab)
startupHook = "/etc/supervisor/conf.d/startup.conf" #Screen startup(supervisord)
startupSh = mypath + "/Record/startup.sh" #Screen startup(supervisord)


streampathSh = mypath + "/Stream/stream.sh" #Stream sh path
streampathXml = mypath +"/Stream/ezstream.xml" #Stream xml path
streampathHook = "/etc/supervisor/conf.d/streamhook.conf" #Stream Hook path


#Installing requirements:

print("Installing requirements ... \n\n")
os.system("sudo apt-get install python3-pyaudio python3-crontab screen")
os.system("sudo apt-get install git-core vim lame madplay ezstream supervisor")
os.system("sudo apt-get install sshpass")
os.system("sudo pip3 install pydub")
os.system("sudo pip3 install -r {}".format(reqpath))
    
#Supervisor
    
with open(streampathHook,'w') as f:
    f.write("""[program:streamhook]
command=/home/pi/Stream/stream.sh
directory=/home/pi/Stream
autostart=true
autorestart=true
startretries=10000
stderr_logfile=/home/pi/Stream/log/streamhook.err.log
stdout_logfile=/home/pi/Stream/log/streamhook.out.log
user=pi
""")
    

with open (startupHook,'w') as f:
    f.write("""[program:startup]
command=/home/pi/Record/startup.sh
directory=/home/pi/Record
autostart=true
autorestart=true
startsecs = 10
startretries=0
stderr_logfile=/home/pi/Record/startuplog/startuphook.err.log
stdout_logfile=/home/pi/Record/startuplog/startuphook.out.log
user=pi
""")
    
#Contab was replaced with supervisord


#Adding permissions and running the scripts

os.system("sudo chmod +x {}".format(startupSh))
os.system("sudo chmod +x {}".format(streampathSh))
os.system("sudo {}".format(startupSh))
os.system("sudo {}".format(streampathSh))
os.system("sudo chmod +x sshserver.sh")

