import time
import socket
import os

#date_tuple = time.localtime()
#time_string = time.strftime("%Y-%m-%d %H.%M.%S", date_tuple)

def is_connected():
    
    try:
        socket.create_connection(("www.google.com", 80))
        print("Connection established")
        return True
    
    except OSError:
        pass

    return False
    print("No connection available")

def update():
    os.system("sudo /etc/init.d/ntp restart")
    
def startup():
    if is_connected() == False:
        while is_connected() == False:
            time.sleep(5)
    else:
        update()
        time.sleep(15)
        date_tuple = time.localtime()
        time = 'time.txt'
        with open(time, 'wb') as f:
            f.write("Day:\nHour:{}".format(time.strftime("%d,%H", date_tuple)))


        

