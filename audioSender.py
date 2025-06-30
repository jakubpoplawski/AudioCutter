from contextlib import suppress
import paramiko

from loggingSettings import logger_wrapper

class SFTPClient():
    
    def __init__(self, port, username, password, ip_list):
        self.host_ip = None
        self.port = port
        self.user = username
        self.password = password
        self.ip_list = ip_list
        self.SSH_Client = paramiko.SSHClient()



    def ssh_connect(self):
        self.SSH_Client.load_system_host_keys()
        self.SSH_Client.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())

        self.SSH_Client.connect(self.host_ip, 
                                username=self.user, 
                                password=self.password,
                                look_for_keys=True,
                                port=self.port,
                                timeout=3)
            
    @logger_wrapper
    def ssh_scan_connect(self):
        for ip in self.ip_list:
            self.host_ip = ip
            with suppress(paramiko.ssh_exception.NoValidConnectionsError):
                try:
                    self.ssh_connect()
                    print(f"Connected to {self.host_ip}:{self.port} as {self.user}.")
                    break
                except Exception as e:
                    raise e

    @logger_wrapper         
    def ssh_disconnect(self):
        self.SSH_Client.close()
        print(f"{self.user} is disconnected from {self.host_ip}:{self.port}")  

    @logger_wrapper
    def ssh_create_directory(self, remote_album_path, mode=770):
        sftp_client = self.SSH_Client.open_sftp()
        if sftp_client.stat(remote_album_path):
            pass
        else:
            try:        
                sftp_client.mkdir(remote_album_path, mode)
            except IOError as e:
                raise e

    @logger_wrapper
    def ssh_upload_file(self, local_track_path, remote_track_path):          
        sftp_client = self.SSH_Client.open_sftp()
        try:
            sftp_client.stat(remote_track_path)
        except FileNotFoundError:  
            try:      
                sftp_client.put(local_track_path, remote_track_path)
            except FileNotFoundError:
                print(f"File {local_track_path} was not found on the local system")

    @logger_wrapper
    def ssh_upload_album(self, track_list, local_album_path, remote_path, album_name):
        remote_album_path = remote_path + album_name.lower() + "/"
        self.ssh_create_directory(remote_album_path)
        for i in range(len(track_list)):
            local_track_path = local_album_path + track_list[i].track_file_name
            remote_track_path = remote_album_path + track_list[i].track_file_name
            self.ssh_upload_file(local_track_path, remote_track_path)
            


