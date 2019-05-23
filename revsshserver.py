import timerequest
import os

rip=False
while True:
    while(timerequest.is_connected()==False):
        rip=False
        print("Waiting for a connection...")
        time.sleep(5)
        
    while(timerequest.is_connected() == True):
        if(rip==False):
            os.system("screen -S sshserver -X quit")
            os.system("sh /home/pi/Ssh/sshserver.sh")
            rip=True
        else:
            pass
            
    
