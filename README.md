# AudioCutter
The below repository contains a command line script cuts a .mp3 audio file into pieces according to indices provided in a .cue file. Audioteka doesn't provide a program for Linux to cut their audiobooks into chapters. Here's a small script that does exatly that.
 
## Overview
The logic of the script is divided in five parts represented with five different modules responsible for extracting data from a .cue file, cutting the .mp3 file, finding the reciever in the local network, and sending the splitted files to the target device.

## Requirments
The Python libraries needed to run the script are specified in the requirements.txt file. External dependencies are FFmpeg to handle file cutting and appending metadata, and nmap for scaning the local network. SSH connections have to be open on the target device - tested with SSH Server mobile app. Termux was used for addtional troubleshooting. 



## argumentParser.py
The ArgumentParser class extracts the arguments from the command and validates the entries. Following arguments can be specified in the command lauching the script:
- path to the local audio file ('-f','--file'), 
- path to the local cuesheet file ('-s','--sheet'),
- path to the local artwork file ('-a','--artwork') (the only non-mandatory argument),
- path to the local folder to store the cut files ('-c','--cut'),
- path to the external folder on the target device to send the files ('-r','--remote').

Checking the existance of the files to which paths were provided and if the files have file type extensions expected in the script logic.

## cueReader.py
The CueReader module uses regex patterns to extract information related to the whole audiobook (stored in CueSheet class) and single tracks (storeed in CueTrack class) in the .cue file. CueSheet class stores a list of CueTrack instances. The regex patterns are stored in the exec_plan attribute of the CueSheet class.

## audioCutter.py
FFmpeg is used to cut the .mp3 file and refine the newly created ones with metadata from the .cue file. Cuts required recalculations from .cue time imndex to miliseconds timestamps.

## ipScanner.py
The IPScanner class takes the port number and IP range and scans the local network for available addresses using nmap. It filters down and transforms the fetched addresses to a list using grep and regex. 

## audioSender.py
The audioSender module contains a SFTPClient class that creates paramiko SSHClient instance. The class takes the credentials to the open SSH server and attempts to establish connection to IP addresses from the recieved from the IPScanner list. The client creates a directory in the target folder on the target device and transfers the cut tracks to that directory. 

