import pyaudio
import wave
import time
import os
import calendar
import shutil
import sys
import socket
from cmd import Cmd
from pydub import AudioSegment
from pathlib import Path
from configparser import SafeConfigParser

import timerequest

if __name__ == "__main__":
    
    form_1 = pyaudio.paInt16 # 16-bit resolution
    chans = 1 # 1 channel
    samp_rate = 44100 # 44.1kHz sampling rate 
    chunk = 4096 # 2^12 samples for buffer
    record_secs = 3600 #seconds to record | 3600 for an hour | 86400 for a day
    dev_index = None # device index found by p.get_device_info_by_index(i)
    file_format = 0 #recording format of audio
    config = SafeConfigParser()
    data_file = "config.ini"
    data_title = "options"
    data_names = ("recording seconds","device id","file format")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_run = False
    
    if (timerequest.is_connected()==False):
        for i in range(3):
            connectivity = timerequest.is_connected()
            if (connectivity==False):
                print("Checking internet connectivity...")
                time.sleep(5)
            else:
                print("Connection established \n")
    
    
    elif (os.path.isfile(str(Path().absolute()) + "/" + data_file)): #Load configurations saved
        data_list = []
        with open(data_file, "r") as f:
            config.read(data_file)
            for x in range(len(data_names)):
                data_list.append(int(config.get(data_title,data_names[x])))
                
            record_secs, dev_index, file_format = data_list #Add new vars
            
    else: #automatically choose the first audio input available
        p = pyaudio.PyAudio()
        for i in range(p.get_device_count()):
            try:
                if (p.get_device_info_by_host_api_device_index(0,i).get("maxInputChannels") > 0):
                    dev_index = i
                    print("\n")
                    print ("Recording device index: {} was automatically selected:{}".format(i, p.get_device_info_by_host_api_device_index(0,i).get("name") + "\n"))
                    break
                else:
                    dev_index = None
                
            except Exception:
                print("\n Exception in channel")
                pass
            
            
    def check_audio_inputs():
        p = pyaudio.PyAudio()
        for i in range(p.get_device_count()):
            print(p.get_device_info_by_index(i).get("name") + " ------> %5s" % (i),)
        
            
    def update_time(request):
        
        date_tuple = time.localtime() # get struct_time
        
        #used for the creation of the folders
        
        if request == "date":
            return date_tuple
        
        #used for the creation of recorded files
        
        elif request == "name":
            if file_format != 0:
                time_name_string = time.strftime("%Y-%m-%d %H.%M.%S", date_tuple)
                return time_name_string
            else:
                time_name_string = time.strftime("%Y%m%d%H%M%S", date_tuple)
                return time_name_string
        
        else:
            raise ValueError("Time update requested isn't corretly specified [name,date]")
        
    def convert(wav_output_filename,time_string,file_path): 
        
        #convert the files from wav to mp3
        
        print("Converting to mp3")
        
        mp3_output_filename= file_path + time_string + ".mp3"
        AudioSegment.from_wav(wav_output_filename).export(mp3_output_filename, format="mp3")
        
        os.remove(wav_output_filename)
        print("Saved file path: " + mp3_output_filename)
        print("Finished recording \n")
        
        
    def check_folders(date_tuple):
        test_path = str(Path().absolute()) #current path
        
        for i in range(3):
            
            if i==0: #year
            
                test_path = test_path + "/" + str(date_tuple[i])
                
                if not os.path.isdir(test_path):
                    os.makedirs(test_path)
                
                else:
                    continue
            
            elif i==1: #month
                
                if file_format != 0: #tree storage
            
                    test_path = test_path + "/" + calendar.month_name[date_tuple[i]]
                    
                    if not os.path.isdir(test_path):
                        os.makedirs(test_path) 
                    else:
                        continue
                
            elif i==2: #day
                
                if file_format != 0:
                    test_path= test_path + "/" + str(date_tuple[i]) + "/"
                    if not os.path.isdir(test_path):
                        os.makedirs(test_path)
                        return test_path
                    else:
                        return test_path
                else:
                    return test_path + "/"
                                
    def is_number(string):
        try:
            int(string)
            return True
        
        except ValueError:
            return False
        
        
    def save_files(content):
        config.read(data_file)
        try:
            config.add_section(data_title)
        except:
            pass
            
        for x in range(len(content)):
            config.set(data_title, data_names[x], str(content[x]))
        
        with open(data_file,"w") as f:
            
            config.write(f)
            
    
    def delete_old_folders():
        date_tuple = update_time("date") #year/month/day
        my_path = str(Path().absolute()) #current path
        test_path = my_path
        if file_format !=0:
        
            for i in range(2):
                
                if i==0: #eliminates old year folders
                    dirs = os.listdir(my_path)
                    test_path = test_path + "/" + str(date_tuple[i])
                    for folders in dirs:
                        folder_path = os.path.abspath(folders)
                        if os.path.isdir(folder_path):
                            if is_number(folders) == True:
                                if int(folders) < date_tuple[i]:
                                    if int(folders) != (date_tuple[i])-1: #check if it's last year
                                        shutil.rmtree (folder_path)
                                        
                                    else: #It's the last year so check January
                                        #check the old folders and files in it| this is missing
                                        continue 
                                else:
                                    continue
                            else:
                                continue
                        else:
                            continue
                        
                elif i==1: #checks for old folders and eliminates old files
                    current_month =  calendar.month_name[date_tuple[i]]
                    
                    if current_month == calendar.month_name[1]: #January
                        break
                    
                    else:
                        
                        months_dir = os.listdir(test_path) #Inside year folder
                        for months in months_dir:                                  
                            now = time.time()
                            folder_path = os.path.abspath(months)
                            #fullpath = os.path.join(dirs, folders)
                            
                            if os.path.isdir(folder_path): #check if its a directory
                                
                                if os.stat(folder_path).st_mtime < (now - (30 * 86400)): # if older than 30 days since last modified
                                    shutil.rmtree(folder_path)
                                    
                                else: #opens that month directory
                                    days = os.listdir(folder_path)
                                    for day in days: #delete
                                        if os.stat(folder_path).st_mtime < (now - (30 * 86400)):
                                            shutil.rmtree(folder_path)
                                        else:
                                            continue
                            else:
                                continue
        else:
            test_path = test_path + "/" + str(date_tuple[0])
            if os.path.isdir(test_path):
                files = [f for f in os.listdir(test_path) if os.path.isfile(f)]
                for f in files:
                    folder_path = os.path.abspath(f)
                    if os.stat(folder_path).st_mtime < (now - (30 * 86400)):
                        os.remove(folder_path)
                    else:
                        continue
                
        
    def record():
        
        audio = pyaudio.PyAudio()
        
        time_string=update_time("name") #update to name the music recording to the present time
        
        folder_path = check_folders(update_time("date")) #compare the existing folders for the present date
        print("Folder path: " + folder_path)
        
        
        frames = []
        
        if socket_run == False:
            try:
                stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                                input_device_index = dev_index,input = True, \
                                frames_per_buffer=chunk)
                
                # loop through stream and append audio chunks to frame array
                for i in range(0,int((samp_rate/chunk)*record_secs)+1):
                    data = stream.read(chunk)
                    frames.append(data)
            
            except OSError:
                return False
        else:
            try:
                stream = audio.open(format=form_1, channels=chans, rate=samp_rate, output=True, frames_per_buffer=chunk)

                t = time.time() + record_secs
                
                while time.time() < t:
                    data = s.recv(chunk)
                    stream.write(data)
                    frames.append(data)
                    
                    
            except (OSError,KeyboardInterrupt,SystemExit):
                    stream.close()
                    audio.terminate()
                    return False                
            
        
        wav_output_filename = folder_path + time_string + ".wav"  # name of .wav file
        print("File name: " + time_string)

        # stop the stream, close it, and terminate the pyaudio instantiation stream
        stream.close()
        audio.terminate()

        #save the audio in .wav files
        wavefile = wave.open(wav_output_filename,"wb")
        wavefile.setnchannels(chans)
        wavefile.setsampwidth(audio.get_sample_size(form_1))
        wavefile.setframerate(samp_rate)
        wavefile.writeframes(b"".join(frames))
        wavefile.close()
        
        print("\nRecording completed")
        
        convert(wav_output_filename,time_string,folder_path) #convert to mp3
            
            
    def main():
        
        print("-----Now recording----- \n")
        
        recording=True
        
        while(recording):
            try:
                print("Recording a new file:")
                delete_old_folders()
                record()
            except KeyboardInterrupt:
                pass
    
    try:
        if sys.argv[1] == "run":
            print("\nAuto running script \n")
            main()
        if sys.argv[1] == "srun":
            inet = sys.argv[2]
            port = int(sys.argv[3])
            s.connect((inet, port))
            socket_run = True
            main()
    except IndexError:
        print("\nManual running \n")
            

class MyPrompt(Cmd):
    prompt = ">"
    
    def do_channels(self,args):
        if args == "":
            check_audio_inputs()
            print("\n")
        else:
            print("This command has no extra options \n")
        
    def do_duration(self,args):
        if args == "help":
            print("Set the time for the recording lenght in seconds \n")
            
        elif is_number(args) == True:
            global record_secs
            record_secs = int(args)
            time = record_secs
            
            if time <= 60:
                print("Recording duration set for %s sec \n" %time)
            
            else:
                secs = time % 10 
                time = record_secs/60
                if time <= 60:
                    print("Recording duration set for {} min and {} sec \n" .format(round(time),round(secs)))
                else:
                    time = time / 60
                    mins = (time %1) *60
                    print("Recording duration set for {} h and {} mins \n" .format(round(time),round(mins)))
            
        else:
            if args != "":
                print("Option not available")
            else:
                print("No duration was selected \nUse [duration help] for assistance \n")
    
    def do_save(self,args):
        
        if dev_index == None:
            print("Please select an audio channel from [channels]\n")

        elif args == "help" or args =="-h" or args == "--help":
            print("Simply [save] to save your prefereces \nThese include: Record duration, channel selected and your file saving preference \n") 
            
        elif args == "":
            save_files((record_secs, dev_index, file_format))
            print("Preferences saved \nDuration(s):{} Channel:{} Storage:{} \n".format(record_secs,dev_index,file_format))
            
        else:
            print("The option to save %s is not available \nUse [save help] to check available options \n" %args)
                
            
    def do_channel(self,args):
        if args == "help":
            print("Select a channel from the available [channels] listed \n")
            
        elif is_number(args) == True:
            global dev_index
            dev_index = int(args)
            print("Channel %s was selected \n" %args)
            
        else:
            if args != "":
                print("%s is not an available channel \n" %args)
            else:
                print("No channel was selected \n")
        
    
    def do_storage(self,args):
        help = "[0] for flat storage and [1] for a tree storage \n"
        if args=="help":
            print(help)
            
        elif is_number(args) == True:
            global file_format
        
            if args == "1":
                print("The file format in tree storage was selected (%s) \n" %args)
                args = int(args)
                file_format = args
                
            elif args == "0":
                print("The file format in flat storage was selected (%s) \n" %args)
                args = int(args)
                file_format = args
                
            else:
                print("This format is not available ")
                print(help)
            
        else:
            print("%s is not an available file storage option" %args)
            print(help)
        
    
    def do_info(self,args):
        print("Duration(s): {}\nChannel: {}\nStorage: {} \n".format(record_secs, dev_index, file_format))
        
        if (file_format == 0):
            print("Flat storage selected \n")
        else:
            print("Tree storage selected \n")
        
    def do_run(self,args):
        if (dev_index==None):
            print("No channel was selected")
        else:
            main()
        
    def do_exit(self,args):
        print ("Closing...")
        raise SystemExit
        
            
    if dev_index == None:
        
        print("\nThere is no recording device being recognized! \nThe audio device number is listed on the right as (index number): \n")
    
        check_audio_inputs()
    
        print("\nSelect the audio channel manual from the ones provided \n[help] for commands \n")
                
    
MyPrompt().cmdloop()
