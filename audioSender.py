import paramiko
import paramiko.ssh_exception
import logging
import re

from loggingSettings import logger_wrapper

logger = logging.getLogger(__name__)

class SFTPClient():
    
    def __init__(self, port, username, password, ip_list):
        """A class to store and initialize the SSHClient class and the 
        functions to initialize the connection with the target device,
        send data, and close the connection.

        Parameters:
            host_ip (txt): IP address for the connection attempt 
                           iterator.
            port (txt): Port used on the target device.
            user (str): User name part of login credentials.            
            password (str): Password part of login credentials.  
            ip_list (list): List of retrived local IP addresses.
            SSH_Client (class): SSH_Client instance.              
        """        
        self.host_ip = None
        self.port = port
        self.user = username
        self.password = password
        self.ip_list = ip_list
        self.SSH_Client = paramiko.SSHClient()


    def ssh_connect(self):
        """The function initializes a SSH connection with an IP address
        using class stored parameters.

        Args:
            None
        
        Returns:
            None          
        """         
        self.SSH_Client.load_system_host_keys()
        self.SSH_Client.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())

        self.SSH_Client.connect(self.host_ip, 
                                username=self.user, 
                                password=self.password,
                                look_for_keys=True,
                                port=self.port)                       
            
    @logger_wrapper
    def ssh_scan_connect(self):
        """The function handles the connection attempts through the list
        of retrived IP addresses.

        Args:
            None
        
        Returns:
            None          
        """         
        for ip in self.ip_list:
            self.host_ip = ip

            try:
                self.ssh_connect()
                break
            except paramiko.ssh_exception.NoValidConnectionsError as e:
                if ip == self.ip_list[-1]:
                    raise e
                continue

    @logger_wrapper         
    def ssh_disconnect(self):
        """The function closes the connection with the target device.

        Args:
            None
        
        Returns:
            None          
        """   
        self.SSH_Client.close()
        logger.info(f"{self.user} is disconnected \
            from {self.host_ip}:{self.port}")  

    @logger_wrapper
    def ssh_create_directory(self, remote_album_path, mode=770):
        """The function checks if a target directory for the cut files 
        exists on the target device. It creates on if it does not exist.

        Args:
            remote_album_path (str): Expected path for the cut files on 
                                     the target device.
            mode (int): access permissions to the created directory.
        
        Returns:
            None          
        """          
        sftp_client = self.SSH_Client.open_sftp()
        try:
            sftp_client.stat(remote_album_path)
            pass
        except IOError as e:
            sftp_client.mkdir(remote_album_path, mode)

    @logger_wrapper
    def ssh_upload_file(self, local_track_path, remote_track_path):
        """The function checks if a file exists on the target device. 
        It sends one if it does not exist.

        Args:
            local_track_path (str): Local path to the file.        
            remote_track_path (str): Expected path for the file on 
                                     the target device.
        
        Returns:
            None          
        """      
        sftp_client = self.SSH_Client.open_sftp()
        try:
            sftp_client.stat(remote_track_path)
            pass
        except IOError as e:
            sftp_client.put(local_track_path, remote_track_path)

    @logger_wrapper
    def ssh_upload_album(self, track_list, local_album_path, 
                         remote_path, album_name, 
                         local_artwork_path=None):
        """The function iterates through the list of gathered tracks 
        and artwork fiel. It handles upload attempts to the target 
        device.

        Args:
            track_list (list): List of collected CueTrack objects.        
            local_album_path (str): Local path to the cut files.
            remote_path (str): Target directory for the files on 
                               the target device.   
            album_name (str): Name to create target directory.   
            local_album_path (str): Local path to the artwork file.                                                 
        
        Returns:
            None          
        """   
        remote_album_path = remote_path + album_name.lower() + "/"
        self.ssh_create_directory(remote_album_path)
        
        for i in range(len(track_list)):
            local_track_path = str(local_album_path) + "/" +\
                track_list[i].track_file_name
            remote_track_path = str(remote_album_path) +\
                track_list[i].track_file_name
            self.ssh_upload_file(local_track_path, remote_track_path)
            
        if local_artwork_path != None:
            artwork_name = re.search(r'[0-9a-zA-Z-]+\.[a-zA-Z-]{2,4}', 
                                     local_artwork_path)
            remote_artwork_path = remote_album_path + \
                                artwork_name.group(0)
            self.ssh_upload_file(local_artwork_path, 
                                 remote_artwork_path)            
            