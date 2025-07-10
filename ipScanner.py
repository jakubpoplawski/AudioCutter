from subprocess import check_output
import logging

from loggingSettings import logger_wrapper

logger = logging.getLogger(__name__)

class IPScanner():
    
    def __init__(self, port, ip_range, regex_ip_filter):
        """A class to store all the data to scan available local IPs 
        with a built nmap command.

        Parameters:
            port (int): IP port set up on target device for access.
            ip_range (txt): Range of IPs 
                            to scan through to find the target device.
            regex_ip_filter (txt): Regex to find IPs via grep command.
        """
        self.port = port
        self.ip_range = ip_range
        self.regex_ip_filter = regex_ip_filter

    
    @logger_wrapper   
    def scan_ips(self):
        """The function builds the nmap/grep command and returns a list 
        of available local IPs.

        Args:
            None
        
        Returns:
            list (list): List of available local IP addresses.           
        """  
        command = f"nmap -sT -p {self.port} "\
            f"{self.ip_range} | grep -oP '{self.regex_ip_filter}'"

        command_result = check_output((command), shell=True).decode()
        
        return list(filter(lambda i: i != '', 
                           command_result.split('\n')))
        