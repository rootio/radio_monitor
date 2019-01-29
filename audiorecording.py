import pyaudio
import wave
import time
import os
import calendar
from pydub import AudioSegment
from pathlib import Path

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate 
chunk = 4096 # 2^12 samples for buffer
record_secs = 10 #seconds to record | 3600 for an hour | 86400 for a day
dev_index = 2 # device index found by p.get_device_info_by_index(i)

    
def update_time(request):
    
    date_tuple = time.localtime() # get struct_time
    
    #used for the creation of the folders
    
    if request == "date":
        return date_tuple
    
    #used for the creation of recorded files
    
    elif request == "name": 
        time_name_string = time.strftime("%d-%m-%Y %H.%M.%S", date_tuple)
        return time_name_string
    
    else:
        raise ValueError("Time update requested isn't corretly specified [name,date]")
    
def convert(wav_output_filename,time_string,file_path): 
    
    #convert the files from wav to mp3
    
    print("Converting to mp3")
    
    mp3_output_filename= file_path + time_string + ".mp3"
    AudioSegment.from_wav(wav_output_filename).export(mp3_output_filename, format="mp3")
    
    os.remove(wav_output_filename)
    
    print("Finished recording \n")
    
    
def check_folders(date_tuple):
    my_path = str(Path().absolute()) #current path
    test_path = my_path
    x=3
    
    for i in date_tuple:
        x -= 1
        
        if x<0: 
            return test_path + "/"
        
        elif x==1: #month
        
            test_path = test_path + "/" + calendar.month_name[i]
            
            if not os.path.isdir(test_path):
                os.makedirs(test_path) 
            else:
                continue
            
        else: #year/day
            test_path = test_path + "/" + str(i)
            
            if not os.path.isdir(test_path):
                os.makedirs(test_path)
            
            else:
                continue
            
def delete_old_folders(date_tuple):
    my_path = str(Path().absolute()) #current path
    test_path = my_path
    
    for i in range(3,0,-1):
        
        if i==2: #eliminates old year folders
            dirs = os.listdir(my_path)
            test_path = test_path + "/" + str(date_tuple[i])
            for folders in dirs:
                folder_path = os.path.abspath(folders)
                if nos.path.isdir(folder_path):
                    if int(folder) < date_tuple[i]:
                        os.remove(folder_path)
                    else:
                        continue
                else:
                    continue
                
        elif i==1: #checks for old folders and eliminates old files
            current_month =  calendar.month_name[date_tuple[i]]
            
            if current_month == "January":
                break
            
            else:
                
                months_dir = os.listdir(test_path)
                for months in months_dir:                                  
                    now = time.time()
                    folder_path = os.path.abspath(months)
                    #fullpath = os.path.join(dirs, folders)
                    
                    if nos.path.isdir(folder_path): #check if its a folder 
                        
                        if os.stat(folder_path).st_mtime < (now - (30 * 86400)): # if older than 30 days since last modified
                             os.remove(folder_path)
                             
                        else: #opens the folder
                            days = os.listdir(folder_path)
                            for day in days:
                                if os.stat(folder_path).st_mtime < (now - (30 * 86400)):
                                    os.remove(folder_path)
                                else:
                                    continue
                    else:
                        continue
                                
    
    
def record():

    audio = pyaudio.PyAudio()
    
    time_string=update_time("name") #update to name the music recording to the present time
    
    folder_path = check_folders(update_time("date")) #compare the existing folders for the present date
    
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)
    
    wav_output_filename = folder_path + time_string + ".wav"  # name of .wav file
    print(time_string)
    
    frames = []

    # loop through stream and append audio chunks to frame array
    for i in range(0,int((samp_rate/chunk)*record_secs)+1):
        data = stream.read(chunk)
        frames.append(data)
    

    # stop the stream, close it, and terminate the pyaudio instantiation stream
    
    stream.close()
    audio.terminate()

    #save the audio in .wav files
    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()
    
    print("\nRecording completed")
    
    convert(wav_output_filename,time_string,folder_path) #convert to mp3
    
        
def main():
    
    print("-----Now recording----- \n")
    
    recording=True
    
    while(recording):
        print("Recording a new file:")
        record()
    
        
main()
    
