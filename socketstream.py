import pyaudio
import socket
import select

p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
  dev = p.get_device_info_by_index(i)
  print((i,dev['name'],dev['maxInputChannels']))

form_1 = pyaudio.paInt16
chans = 1
samp_rate = 44100
chunk = 4096
dev_index = 2


for i in range(p.get_device_count()):
    try:
        if (p.get_device_info_by_host_api_device_index(0,i).get("maxInputChannels") > 0):
            dev_index = i
            print("\n")
            print ("Recording device index: {} was automatically selected:{}".format(i, p.get_device_info_by_host_api_device_index(0,i).get("name") + "\n"))
            break
        else:
            dev_index = 2
            
    except Exception:
        print("\n Exception in channel")
        pass


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('', 4445))
serversocket.listen(5)


def callback(in_data, frame_count, time_info, status):
    for s in read_list[1:]:
        s.send(in_data)
    return (None, pyaudio.paContinue)


# start Recording
try:
    stream = p.open(format=form_1, channels=chans, rate=samp_rate, input=True,input_device_index = dev_index, frames_per_buffer=chunk, stream_callback=callback)
except Exception as f:
    print(f)

read_list = [serversocket]
print ("Socket created")

try:
    while True:
        readable, writable, errored = select.select(read_list, [], [])
        for s in readable:
            if s is serversocket:
                (clientsocket, address) = serversocket.accept()
                read_list.append(clientsocket)
                print ("Connection from", address)
            else:
                data = s.recv(1024)
                if data == '':
                    data = silence = chr(0)*self.chunk*self.channels*2
                                
                stream.write(data) 
            
except (OSError,KeyboardInterrupt,SystemExit):
    print ("\nEnded socket")
    serversocket.close()
    stream.stop_stream()
    stream.close()
    p.terminate()
    